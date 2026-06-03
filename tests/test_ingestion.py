import json
from pathlib import Path

from src.glowfit.ingestion import ingest_amazon_beauty_jsonl


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )


def test_ingest_amazon_beauty_jsonl_writes_processed_artifacts(tmp_path):
    metadata_path = tmp_path / "metadata.jsonl"
    reviews_path = tmp_path / "reviews.jsonl"
    output_dir = tmp_path / "processed"
    _write_jsonl(
        metadata_path,
        [
            {
                "asin": "B001",
                "title": "Barrier Gel Cream",
                "brand": "Aster Lab",
                "price": "$24.00",
                "average_rating": 4.6,
                "rating_number": 1180,
                "features": ["Fragrance free", "Light texture"],
                "categories": [["Beauty", "Skin Care", "Moisturizers"]],
            },
            {
                "asin": "BOOK1",
                "title": "A Novel",
                "categories": [["Books", "Fiction"]],
            },
        ],
    )
    _write_jsonl(
        reviews_path,
        [
            {
                "reviewerID": "A1",
                "asin": "B001",
                "overall": 5,
                "reviewText": "Light and soothing.",
                "unixReviewTime": 1735689600,
            },
            {
                "reviewerID": "A2",
                "asin": "BOOK1",
                "overall": 5,
                "reviewText": "Not a beauty product.",
                "unixReviewTime": 1735689600,
            },
        ],
    )

    summary = ingest_amazon_beauty_jsonl(
        metadata_path=metadata_path,
        reviews_path=reviews_path,
        output_dir=output_dir,
        limit=10,
    )

    assert summary == {
        "products_written": 1,
        "reviews_written": 1,
        "products_path": str(output_dir / "products.json"),
        "reviews_path": str(output_dir / "reviews.json"),
    }
    products = json.loads((output_dir / "products.json").read_text(encoding="utf-8"))
    reviews = json.loads((output_dir / "reviews.json").read_text(encoding="utf-8"))
    assert products[0]["product_id"] == "B001"
    assert reviews[0]["product_id"] == "B001"
