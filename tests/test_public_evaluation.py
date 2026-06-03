import json
from pathlib import Path

from src.glowfit.public_evaluation import (
    build_public_artifact_evaluation_report,
    write_public_artifact_evaluation_report,
)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_build_public_artifact_evaluation_report_uses_review_threshold(tmp_path: Path):
    _write_json(
        tmp_path / "products.json",
        [
            {
                "product_id": "p1",
                "name": "Barrier Gel",
                "category": "moisturizer",
                "brand": "Aster",
                "price_usd": 20.0,
                "average_rating": 4.5,
                "review_count": 10,
                "attributes": ["light texture", "fragrance free", "barrier care"],
            },
            {
                "product_id": "p2",
                "name": "Heavy Cream",
                "category": "moisturizer",
                "brand": "Mira",
                "price_usd": 32.0,
                "average_rating": 3.2,
                "review_count": 3,
                "attributes": ["rich texture", "strong scent"],
            },
        ],
    )
    _write_json(
        tmp_path / "reviews.json",
        [
            {
                "review_id": "r1",
                "user_id": "u1",
                "product_id": "p1",
                "rating": 5,
                "text": "Light and fragrance free for dry skin.",
                "timestamp": "2020-01-01",
            },
            {
                "review_id": "r2",
                "user_id": "u2",
                "product_id": "p2",
                "rating": 3,
                "text": "Too scented.",
                "timestamp": "2020-01-02",
            },
        ],
    )

    report = build_public_artifact_evaluation_report(
        artifact_dir=tmp_path,
        relevant_rating_threshold=4,
        k_values=[1, 2],
    )

    assert report["artifact_dir"] == str(tmp_path)
    assert report["product_count"] == 2
    assert report["review_count"] == 2
    assert report["relevance_rule"] == "review_rating >= 4"
    assert report["relevant_product_ids"] == ["p1"]
    assert report["models"]["hybrid"]["ranked_product_ids"][0] == "p1"
    assert report["models"]["hybrid"]["metrics"]["precision@1"] == 1.0
    assert set(report["models"]) == {
        "popularity",
        "rating",
        "collaborative",
        "content",
        "two_tower",
        "hybrid",
    }


def test_write_public_artifact_evaluation_report_creates_parent_directory(tmp_path: Path):
    _write_json(
        tmp_path / "products.json",
        [
            {
                "product_id": "p1",
                "name": "Barrier Gel",
                "category": "moisturizer",
                "brand": "Aster",
                "price_usd": 20.0,
                "average_rating": 4.5,
                "review_count": 10,
                "attributes": ["light texture", "fragrance free", "barrier care"],
            }
        ],
    )
    _write_json(
        tmp_path / "reviews.json",
        [
            {
                "review_id": "r1",
                "user_id": "u1",
                "product_id": "p1",
                "rating": 5,
                "text": "Light and fragrance free for dry skin.",
                "timestamp": "2020-01-01",
            }
        ],
    )

    output_path = tmp_path / "reports" / "public_evaluation.json"
    report = write_public_artifact_evaluation_report(
        artifact_dir=tmp_path,
        output_path=output_path,
    )

    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["models"]["hybrid"]["ranked_product_ids"] == ["p1"]
    assert report == written
