from __future__ import annotations

import argparse
import json
from typing import Any
from urllib.request import Request, urlopen


def _request(url: str, payload: dict[str, object] | None = None) -> bytes:
    request = Request(url, method="POST" if payload is not None else "GET")
    if payload is not None:
        request.add_header("Content-Type", "application/json")
        request.data = json.dumps(payload).encode("utf-8")
    with urlopen(request, timeout=15) as response:  # noqa: S310 - CI URLs are explicit arguments
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return response.read()


def _request_json(url: str, payload: dict[str, object] | None = None) -> dict[str, Any]:
    return json.loads(_request(url, payload).decode("utf-8"))


def verify_deployment(api_base_url: str, frontend_url: str) -> None:
    api_base = api_base_url.rstrip("/")
    health = _request_json(f"{api_base}/health")
    if health.get("status") != "ok" or not isinstance(health.get("product_count"), int):
        raise RuntimeError("API health response is incomplete")

    recommendations = _request_json(
        f"{api_base}/recommendations",
        {
            "preferences": {
                "skin_type": "dry",
                "concerns": ["redness", "barrier care"],
                "texture": "light",
                "fragrance_sensitivity": "high",
                "budget_max_usd": 25,
                "avoid": ["strong scent"],
            },
            "limit": 1,
        },
    )
    items = recommendations.get("recommendations")
    if not isinstance(items, list) or not items:
        raise RuntimeError("Recommendation response is empty")
    first_item = items[0]
    if "evidence_strength" not in first_item or "hash_similarity" not in first_item.get(
        "model_scores", {}
    ):
        raise RuntimeError("Recommendation response does not match the deployed contract")

    _request(frontend_url.rstrip("/"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify deployed GlowFit frontend and API endpoints."
    )
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--frontend-url", required=True)
    args = parser.parse_args()
    verify_deployment(args.api_base_url, args.frontend_url)
    print("Deployment smoke check passed.")


if __name__ == "__main__":
    main()
