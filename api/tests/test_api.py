from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_endpoint_returns_loaded_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["product_count"] == 3


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
