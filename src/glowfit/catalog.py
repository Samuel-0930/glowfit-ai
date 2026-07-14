from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.glowfit.data import load_products, load_reviews
from src.glowfit.schemas import Product, Review


@dataclass(frozen=True)
class Catalog:
    products: tuple[Product, ...]
    reviews: tuple[Review, ...]
    source: str


class CatalogRepository(Protocol):
    def load(self) -> Catalog: ...


class CatalogUnavailableError(RuntimeError):
    """Raised when the configured catalog cannot be reached."""


@dataclass
class CachedCatalogRepository:
    repository: CatalogRepository
    ttl_seconds: float
    _catalog: Catalog | None = None
    _expires_at: float = 0.0
    _lock: Lock = field(default_factory=Lock)
    _refresh_lock: Lock = field(default_factory=Lock)

    def load(self) -> Catalog:
        while True:
            with self._lock:
                if self._catalog is not None and time.monotonic() < self._expires_at:
                    return self._catalog
                stale_catalog = self._catalog

            if self._refresh_lock.acquire(blocking=False):
                break
            if stale_catalog is not None:
                return stale_catalog
            with self._refresh_lock:
                pass

        try:
            try:
                catalog = self.repository.load()
            except (HTTPError, TimeoutError, URLError, ValueError, KeyError, TypeError) as error:
                if stale_catalog is not None:
                    return stale_catalog
                raise CatalogUnavailableError(
                    "The catalog data source is temporarily unavailable."
                ) from error

            with self._lock:
                self._catalog = catalog
                self._expires_at = time.monotonic() + self.ttl_seconds
                return catalog
        finally:
            self._refresh_lock.release()


@dataclass(frozen=True)
class JsonCatalogRepository:
    data_dir: Path

    def load(self) -> Catalog:
        return Catalog(
            products=tuple(load_products(self.data_dir / "products.json")),
            reviews=tuple(load_reviews(self.data_dir / "reviews.json")),
            source="sample_data",
        )


@dataclass(frozen=True)
class SupabaseCatalogRepository:
    url: str
    api_key: str

    def _select(self, table: str, columns: str) -> list[dict[str, object]]:
        headers = {"apikey": self.api_key}
        if not self.api_key.startswith("sb_secret_"):
            headers["Authorization"] = f"Bearer {self.api_key}"
        order = {
            "products": "product_id.asc",
            "product_tags": "product_id.asc,tag.asc",
            "reviews": "review_id.asc",
        }[table]
        page_size = 1000
        rows: list[dict[str, object]] = []
        offset = 0

        while True:
            query = urlencode(
                {"select": columns, "order": order, "limit": page_size, "offset": offset}
            )
            request = Request(
                f"{self.url.rstrip('/')}/rest/v1/{table}?{query}",
                headers=headers,
            )
            with urlopen(request, timeout=10) as response:  # noqa: S310 - configured Supabase URL
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, list):
                raise ValueError(f"Expected a list response from Supabase table {table}")
            rows.extend(payload)
            if len(payload) < page_size:
                return rows
            offset += page_size

    def load(self) -> Catalog:
        products = self._select(
            "products",
            "product_id,name,category,brand,price_usd,average_rating,review_count",
        )
        tags = self._select("product_tags", "product_id,tag")
        reviews = self._select("reviews", "review_id,user_id,product_id,rating,text,reviewed_on")

        attributes_by_product: dict[str, list[str]] = {}
        for row in tags:
            product_id = str(row["product_id"])
            attributes_by_product.setdefault(product_id, []).append(str(row["tag"]))

        return Catalog(
            products=tuple(
                Product.model_validate(
                    {
                        **row,
                        "attributes": attributes_by_product.get(str(row["product_id"]), []),
                    }
                )
                for row in products
            ),
            reviews=tuple(
                Review.model_validate(
                    {
                        **{key: value for key, value in row.items() if key != "reviewed_on"},
                        "timestamp": row["reviewed_on"],
                    }
                )
                for row in reviews
            ),
            source="supabase",
        )


def get_catalog_repository() -> CatalogRepository:
    source = os.getenv("GLOWFIT_CATALOG_SOURCE", "json")
    if source == "json":
        return JsonCatalogRepository(Path("sample_data"))
    if source != "supabase":
        raise ValueError("GLOWFIT_CATALOG_SOURCE must be either 'json' or 'supabase'")

    url = os.getenv("SUPABASE_URL")
    api_key = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not api_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SECRET_KEY or SUPABASE_SERVICE_ROLE_KEY are required when "
            "GLOWFIT_CATALOG_SOURCE=supabase"
        )
    return SupabaseCatalogRepository(url=url, api_key=api_key)
