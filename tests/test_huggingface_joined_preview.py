import json
from pathlib import Path

from src.glowfit.huggingface_joined_preview import (
    fetch_and_write_joined_huggingface_preview,
    fetch_huggingface_search_rows,
)
from tests.test_huggingface_preview import FakeResponse


def test_fetch_huggingface_search_rows_builds_dataset_viewer_request():
    seen_urls: list[str] = []

    def fake_urlopen(url: str, timeout: int):
        seen_urls.append(url)
        assert timeout == 20
        return FakeResponse({"rows": [{"row": {"parent_asin": "B001"}}]})

    rows = fetch_huggingface_search_rows(
        dataset="owner/dataset",
        config="default",
        split="train",
        query="B001",
        offset=0,
        length=3,
        urlopen=fake_urlopen,
    )

    assert rows == [{"parent_asin": "B001"}]
    assert seen_urls == [
        "https://datasets-server.huggingface.co/search?"
        "dataset=owner%2Fdataset&config=default&split=train&query=B001&offset=0&length=3"
    ]


def test_fetch_huggingface_search_rows_returns_empty_rows_on_timeout():
    def fake_urlopen(url: str, timeout: int):
        raise TimeoutError("search index timed out")

    rows = fetch_huggingface_search_rows(
        dataset="owner/dataset",
        config="default",
        split="train",
        query="B001",
        offset=0,
        length=3,
        urlopen=fake_urlopen,
    )

    assert rows == []


def test_fetch_and_write_joined_huggingface_preview_matches_reviews_by_asin(tmp_path: Path):
    review_pages = {
        0: [
            {
                "asin": "B001",
                "rating": 5,
                "text": "Light and calming.",
                "user_id": "A1",
                "timestamp": "2020-05-05 14:08:48.923",
            },
            {
                "asin": "B404",
                "rating": 3,
                "text": "Could not find matching metadata.",
                "user_id": "A2",
                "timestamp": "2020-05-06 14:08:48.923",
            },
        ],
        2: [
            {
                "asin": "B002",
                "rating": 4,
                "text": "Soft texture, no irritation.",
                "user_id": "A3",
                "timestamp": "2020-05-07 14:08:48.923",
            }
        ],
    }
    metadata_rows = {
        "B001": [
            {
                "parent_asin": "B001",
                "title": "Barrier Gel Cream",
                "store": "Aster Lab",
                "price": 24.0,
                "average_rating": 4.6,
                "rating_number": 1180,
                "features": "Fragrance free. Light texture.",
                "categories": ["Beauty", "Skin Care", "Moisturizers"],
            }
        ],
        "B002": [
            {
                "parent_asin": "B002",
                "title": "Soft Milk Cleanser",
                "store": "Mira",
                "price": 18.0,
                "average_rating": 4.4,
                "rating_number": 620,
                "features": "Gentle cleanser. Low pH.",
                "categories": ["Beauty", "Skin Care", "Cleansers"],
            }
        ],
    }

    def fake_fetch_rows(dataset: str, config: str, split: str, offset: int, length: int):
        assert dataset == "reviews"
        assert config == "default"
        assert split == "train"
        assert length == 2
        return review_pages.get(offset, [])

    def fake_search_rows(
        dataset: str, config: str, split: str, query: str, offset: int, length: int
    ):
        assert dataset == "metadata"
        assert offset == 0
        assert length == 5
        return metadata_rows.get(query, [])

    summary = fetch_and_write_joined_huggingface_preview(
        output_dir=tmp_path,
        metadata_dataset="metadata",
        reviews_dataset="reviews",
        target_matches=2,
        review_page_size=2,
        max_review_rows=4,
        fetch_rows=fake_fetch_rows,
        search_rows=fake_search_rows,
    )

    products = json.loads((tmp_path / "products.json").read_text(encoding="utf-8"))
    reviews = json.loads((tmp_path / "reviews.json").read_text(encoding="utf-8"))
    summary_payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert [product["product_id"] for product in products] == ["B001", "B002"]
    assert [review["product_id"] for review in reviews] == ["B001", "B002"]
    assert summary["products_written"] == 2
    assert summary["reviews_written"] == 2
    assert summary["review_rows_scanned"] == 3
    assert summary["metadata_searches"] == 3
    assert summary_payload["target_matches"] == 2
