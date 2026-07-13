from scripts import smoke_deployment


def test_verify_deployment_checks_api_contract_and_frontend(monkeypatch):
    responses = [
        {"status": "ok", "product_count": 3},
        {
            "recommendations": [
                {
                    "evidence_strength": 0.8,
                    "model_scores": {"hash_similarity": 0.7},
                }
            ]
        },
    ]
    requested_urls: list[str] = []

    def fake_request_json(url: str, payload=None):
        requested_urls.append(url)
        return responses.pop(0)

    frontend_urls: list[str] = []
    monkeypatch.setattr(smoke_deployment, "_request_json", fake_request_json)
    monkeypatch.setattr(smoke_deployment, "_request", lambda url: frontend_urls.append(url))

    smoke_deployment.verify_deployment(
        api_base_url="https://api.example/",
        frontend_url="https://app.example/",
    )

    assert requested_urls == [
        "https://api.example/health",
        "https://api.example/recommendations",
    ]
    assert frontend_urls == ["https://app.example"]
