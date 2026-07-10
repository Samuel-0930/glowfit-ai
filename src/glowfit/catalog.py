from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
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
    service_role_key: str

    def _select(self, table: str, columns: str) -> list[dict[str, object]]:
        query = urlencode({"select": columns})
        request = Request(
            f"{self.url.rstrip('/')}/rest/v1/{table}?{query}",
            headers={
                "apikey": self.service_role_key,
                "Authorization": f"Bearer {self.service_role_key}",
            },
        )
        with urlopen(request, timeout=10) as response:  # noqa: S310 - configured Supabase URL
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, list):
            raise ValueError(f"Expected a list response from Supabase table {table}")
        return payload

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
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required when "
            "GLOWFIT_CATALOG_SOURCE=supabase"
        )
    return SupabaseCatalogRepository(url=url, service_role_key=service_role_key)
