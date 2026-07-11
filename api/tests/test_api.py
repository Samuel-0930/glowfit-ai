from fastapi.testclient import TestClient

from api.main import app

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
    assert body["recommendations"][0]["model_scores"]["two_tower"] >= 0


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
