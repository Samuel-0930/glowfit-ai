import json
from pathlib import Path
from urllib.error import HTTPError

import pytest

from src.glowfit.huggingface_preview import (
    HuggingFaceDatasetUnavailable,
    fetch_huggingface_rows,
    write_huggingface_preview,
)


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_fetch_huggingface_rows_builds_dataset_viewer_request():
    seen_urls: list[str] = []

    def fake_urlopen(url: str, timeout: int):
        seen_urls.append(url)
        assert timeout == 20
        return FakeResponse({"rows": [{"row": {"asin": "B001"}}]})

    rows = fetch_huggingface_rows(
        dataset="owner/dataset",
        config="default",
        split="train",
        offset=5,
        length=10,
        urlopen=fake_urlopen,
    )

    assert rows == [{"asin": "B001"}]
    assert seen_urls == [
        "https://datasets-server.huggingface.co/rows?"
        "dataset=owner%2Fdataset&config=default&split=train&offset=5&length=10"
    ]


def test_fetch_huggingface_rows_wraps_viewer_outage():
    def failing_urlopen(url: str, timeout: int):
        raise HTTPError(url, 503, "Service Unavailable", {}, None)

    with pytest.raises(HuggingFaceDatasetUnavailable, match="Try again later"):
        fetch_huggingface_rows(
            dataset="owner/dataset",
            config="default",
            split="train",
            offset=0,
            length=1,
            urlopen=failing_urlopen,
        )


def test_write_huggingface_preview_maps_real_dataset_shapes(tmp_path: Path):
    metadata_rows = [
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
    ]
    review_rows = [
        {
            "asin": "B001",
            "rating": 5,
            "text": "Light and soothing for dry skin.",
            "user_id": "A1",
            "timestamp": "2020-05-05 14:08:48.923",
        }
    ]

    summary = write_huggingface_preview(
        metadata_rows=metadata_rows,
        review_rows=review_rows,
        output_dir=tmp_path,
    )

    products = json.loads((tmp_path / "products.json").read_text(encoding="utf-8"))
    reviews = json.loads((tmp_path / "reviews.json").read_text(encoding="utf-8"))
    assert summary["products_written"] == 1
    assert summary["reviews_written"] == 1
    assert products[0]["product_id"] == "B001"
    assert products[0]["brand"] == "Aster Lab"
    assert reviews[0]["review_id"] == "hf_B001_1"
    assert reviews[0]["timestamp"] == "2020-05-05"
