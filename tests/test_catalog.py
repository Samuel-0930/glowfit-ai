from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse

from src.glowfit.catalog import (
    CachedCatalogRepository,
    CatalogUnavailableError,
    JsonCatalogRepository,
    SupabaseCatalogRepository,
    get_catalog_repository,
)


def test_json_catalog_repository_loads_sample_data() -> None:
    catalog = JsonCatalogRepository(Path("sample_data")).load()

    assert catalog.source == "sample_data"
    assert len(catalog.products) == 3
    assert len(catalog.reviews) == 5
    assert catalog.products[0].attributes == [
        "light texture",
        "fragrance free",
        "dry skin",
        "barrier care",
    ]


def test_catalog_repository_rejects_unknown_source(monkeypatch: Any) -> None:
    monkeypatch.setenv("GLOWFIT_CATALOG_SOURCE", "unknown")

    try:
        get_catalog_repository()
    except ValueError as error:
        assert str(error) == "GLOWFIT_CATALOG_SOURCE must be either 'json' or 'supabase'"
    else:
        raise AssertionError("Expected an invalid catalog source to raise ValueError")


def test_supabase_catalog_repository_rebuilds_product_attributes(
    monkeypatch: Any,
) -> None:
    payloads = {
        "products": [
            {
                "product_id": "p_1",
                "name": "Test Cream",
                "category": "moisturizer",
                "brand": "GlowFit",
                "price_usd": 20,
                "average_rating": 4.5,
                "review_count": 3,
            }
        ],
        "product_tags": [
            {"product_id": "p_1", "tag": "dry skin"},
            {"product_id": "p_1", "tag": "fragrance free"},
        ],
        "reviews": [
            {
                "review_id": "r_1",
                "user_id": "u_1",
                "product_id": "p_1",
                "rating": 5,
                "text": "Comfortable on dry skin.",
                "reviewed_on": "2025-01-01",
            }
        ],
    }

    class FakeResponse:
        def __init__(self, payload: object) -> None:
            self.payload = payload

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(self.payload).encode("utf-8")

    def fake_urlopen(request: Any, timeout: int) -> FakeResponse:
        parsed_url = urlparse(request.full_url)
        table = parsed_url.path.split("/rest/v1/")[1]
        query = parse_qs(parsed_url.query)
        assert timeout == 10
        assert request.headers["Apikey"] == "sb_secret_test-key"
        assert "Authorization" not in request.headers
        offset = int(query["offset"][0])
        limit = int(query["limit"][0])
        return FakeResponse(payloads[table][offset : offset + limit])

    monkeypatch.setattr("src.glowfit.catalog.urlopen", fake_urlopen)

    catalog = SupabaseCatalogRepository(
        url="https://example.supabase.co", api_key="sb_secret_test-key"
    ).load()

    assert catalog.source == "supabase"
    assert catalog.products[0].attributes == ["dry skin", "fragrance free"]
    assert catalog.reviews[0].timestamp == "2025-01-01"


def test_supabase_catalog_repository_reads_all_pages(monkeypatch: Any) -> None:
    rows = [{"review_id": f"r_{index}"} for index in range(1001)]
    offsets: list[int] = []

    class FakeResponse:
        def __init__(self, payload: object) -> None:
            self.payload = payload

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(self.payload).encode("utf-8")

    def fake_urlopen(request: Any, timeout: int) -> FakeResponse:
        query = parse_qs(urlparse(request.full_url).query)
        offset = int(query["offset"][0])
        offsets.append(offset)
        assert query["order"] == ["review_id.asc"]
        return FakeResponse(rows[offset : offset + int(query["limit"][0])])

    monkeypatch.setattr("src.glowfit.catalog.urlopen", fake_urlopen)
    repository = SupabaseCatalogRepository(
        url="https://example.supabase.co", api_key="sb_secret_test-key"
    )

    assert repository._select("reviews", "review_id") == rows
    assert offsets == [0, 1000]


def test_supabase_catalog_repository_uses_bearer_header_for_legacy_key(
    monkeypatch: Any,
) -> None:
    class FakeResponse:
        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def read(self) -> bytes:
            return b"[]"

    def fake_urlopen(request: Any, timeout: int) -> FakeResponse:
        assert timeout == 10
        assert request.headers["Authorization"] == "Bearer legacy-service-role-key"
        return FakeResponse()

    monkeypatch.setattr("src.glowfit.catalog.urlopen", fake_urlopen)

    catalog = SupabaseCatalogRepository(
        url="https://example.supabase.co", api_key="legacy-service-role-key"
    ).load()

    assert catalog.products == ()
    assert catalog.reviews == ()


def test_cached_catalog_repository_uses_one_load_within_ttl() -> None:
    class FakeRepository:
        calls = 0

        def load(self):
            self.calls += 1
            return JsonCatalogRepository(Path("sample_data")).load()

    repository = FakeRepository()
    catalog = CachedCatalogRepository(repository=repository, ttl_seconds=60)

    assert catalog.load() is catalog.load()
    assert repository.calls == 1


def test_cached_catalog_repository_raises_clear_error_when_source_is_unavailable() -> None:
    class OfflineRepository:
        def load(self):
            raise URLError("offline")

    catalog = CachedCatalogRepository(repository=OfflineRepository(), ttl_seconds=60)

    try:
        catalog.load()
    except CatalogUnavailableError as error:
        assert "temporarily unavailable" in str(error)
    else:
        raise AssertionError("Expected unavailable catalog error")


def test_cached_catalog_repository_serves_stale_catalog_when_refresh_fails() -> None:
    class FlakyRepository:
        calls = 0

        def load(self):
            self.calls += 1
            if self.calls == 1:
                return JsonCatalogRepository(Path("sample_data")).load()
            raise URLError("offline")

    repository = FlakyRepository()
    catalog = CachedCatalogRepository(repository=repository, ttl_seconds=0)

    initial = catalog.load()
    assert catalog.load() is initial
    assert repository.calls == 2
