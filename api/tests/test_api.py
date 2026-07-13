from fastapi.testclient import TestClient

from api import main
from api.main import app
from src.glowfit.catalog import CatalogUnavailableError

client = TestClient(app)


def test_health_endpoint_returns_loaded_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["product_count"] == 3


def test_recommendations_endpoint_allows_local_frontend_origin():
    response = client.options(
        "/recommendations",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert response.headers.get("access-control-allow-credentials") != "true"


def test_recommendations_endpoint_rejects_unlisted_origin():
    response = client.options(
        "/recommendations",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_cors_origins_strips_whitespace(monkeypatch):
    monkeypatch.setenv("GLOWFIT_CORS_ORIGINS", "https://app.example, https://preview.example, ")

    assert main.cors_origins() == ["https://app.example", "https://preview.example"]


def test_production_configuration_requires_trusted_hosts(monkeypatch):
    monkeypatch.setenv("GLOWFIT_ENV", "production")
    monkeypatch.delenv("GLOWFIT_TRUSTED_HOSTS", raising=False)

    assert main.is_production()
    assert main.trusted_hosts() == []


def test_catalog_cache_ttl_requires_a_finite_non_negative_number(monkeypatch):
    monkeypatch.setenv("GLOWFIT_CATALOG_CACHE_TTL_SECONDS", "NaN")

    try:
        main.catalog_cache_ttl_seconds()
    except RuntimeError as error:
        assert "non-negative number" in str(error)
    else:
        raise AssertionError("Expected an invalid cache TTL to be rejected")


def test_api_docs_are_disabled_for_production(monkeypatch):
    monkeypatch.setenv("GLOWFIT_ENV", "production")
    assert not main.api_docs_enabled()

    monkeypatch.setenv("GLOWFIT_ENV", "development")
    assert main.api_docs_enabled()


def test_health_returns_503_when_catalog_is_unavailable(monkeypatch):
    class OfflineRepository:
        def load(self):
            raise CatalogUnavailableError("offline")

    monkeypatch.setattr(main, "_catalog_repository", OfflineRepository())

    response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body == {
        "detail": "추천 카탈로그에 일시적으로 연결할 수 없습니다. 잠시 후 다시 시도해 주세요."
    }
    assert "offline" not in str(body)
    assert "secret" not in str(body).lower()
    assert "http" not in str(body).lower()


def test_recommendations_reject_invalid_profile_fields():
    response = client.post(
        "/recommendations",
        json={
            "preferences": {
                "skin_type": "unknown",
                "concerns": ["redness"],
                "texture": "light",
                "fragrance_sensitivity": "high",
                "budget_max_usd": 25,
                "avoid": [],
            }
        },
    )

    assert response.status_code == 422


def test_recommendations_reject_oversized_preference_terms():
    response = client.post(
        "/recommendations",
        json={
            "preferences": {
                "skin_type": "dry",
                "concerns": ["redness"] * 11,
                "texture": "light",
                "fragrance_sensitivity": "high",
                "budget_max_usd": 25,
                "avoid": [],
            }
        },
    )

    assert response.status_code == 422


def test_compare_rejects_more_than_twenty_product_ids():
    response = client.post("/compare", json={"product_ids": [f"p_{index}" for index in range(21)]})

    assert response.status_code == 422


def test_recommend_endpoint_returns_top_products():
    payload = {
        "skin_type": "dry",
        "concerns": ["redness", "barrier care"],
        "texture": "light",
        "fragrance_sensitivity": "high",
        "budget_max_usd": 25,
        "avoid": ["strong scent", "sticky finish"],
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"][0]["product"]["product_id"] == "p_glow_gel"
    assert body["recommendations"][0]["evidence"]


def test_recommendations_endpoint_returns_report_contract():
    payload = {
        "preferences": {
            "skin_type": "dry",
            "concerns": ["redness", "barrier care"],
            "texture": "light",
            "fragrance_sensitivity": "high",
            "budget_max_usd": 25,
            "avoid": ["strong scent", "sticky finish"],
        },
        "limit": 2,
    }

    response = client.post("/recommendations", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["generation_mode"] == "api-hybrid-ranking"
    assert body["metadata"]["data_source"] == "sample_data"
    assert body["metadata"]["requested_limit"] == 2
    assert body["metadata"]["returned_count"] == 2
    assert body["metadata"]["top_product_id"] == "p_glow_gel"
    assert body["recommendations"][0]["model_scores"]["hash_similarity"] >= 0
    assert body["recommendations"][0]["evidence_strength"] >= 0


def test_report_endpoint_returns_grounded_sections():
    payload = {
        "skin_type": "dry",
        "concerns": ["redness", "barrier care"],
        "texture": "light",
        "fragrance_sensitivity": "high",
        "budget_max_usd": 25,
        "avoid": ["strong scent", "sticky finish"],
    }

    response = client.post("/report", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "summary" in body
    assert "recommendations" in body
    assert body["generation_mode"] == "deterministic"
