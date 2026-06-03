from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen as default_urlopen

from src.glowfit.datasets import parse_amazon_metadata_record
from src.glowfit.schemas import Product, Review

DATASET_VIEWER_BASE_URL = "https://datasets-server.huggingface.co"


def fetch_huggingface_rows(
    dataset: str,
    config: str,
    split: str,
    offset: int,
    length: int,
    urlopen: Callable[..., Any] = default_urlopen,
) -> list[dict[str, Any]]:
    query = urlencode(
        {
            "dataset": dataset,
            "config": config,
            "split": split,
            "offset": offset,
            "length": length,
        }
    )
    url = f"{DATASET_VIEWER_BASE_URL}/rows?{query}"
    with urlopen(url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [item["row"] for item in payload.get("rows", [])]


def _metadata_row_to_product(row: dict[str, Any]) -> Product:
    return parse_amazon_metadata_record(row)


def _review_row_to_review(row: dict[str, Any], index: int) -> Review:
    product_id = str(row.get("asin") or row.get("parent_asin"))
    raw_timestamp = str(row.get("timestamp") or row.get("reviewTime") or "")
    timestamp = raw_timestamp[:10] if len(raw_timestamp) >= 10 else "1970-01-01"
    return Review(
        review_id=f"hf_{product_id}_{index}",
        user_id=str(row.get("user_id") or row.get("reviewerID") or "unknown"),
        product_id=product_id,
        rating=int(row.get("rating") or row.get("overall") or 0),
        text=str(row.get("text") or row.get("reviewText") or row.get("title") or ""),
        timestamp=timestamp,
    )


def write_huggingface_preview(
    metadata_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    output_dir: Path,
) -> dict[str, str | int]:
    products = [_metadata_row_to_product(row) for row in metadata_rows]
    reviews = [_review_row_to_review(row, index) for index, row in enumerate(review_rows, start=1)]

    output_dir.mkdir(parents=True, exist_ok=True)
    products_path = output_dir / "products.json"
    reviews_path = output_dir / "reviews.json"
    products_path.write_text(
        json.dumps([product.model_dump() for product in products], indent=2),
        encoding="utf-8",
    )
    reviews_path.write_text(
        json.dumps([review.model_dump() for review in reviews], indent=2),
        encoding="utf-8",
    )
    return {
        "products_written": len(products),
        "reviews_written": len(reviews),
        "products_path": str(products_path),
        "reviews_path": str(reviews_path),
    }


def fetch_and_write_huggingface_preview(
    output_dir: Path,
    metadata_dataset: str = "smartcat/Amazon_All_Beauty_2023",
    reviews_dataset: str = "jhan21/amazon-beauty-reviews-dataset",
    config: str = "default",
    split: str = "train",
    offset: int = 0,
    length: int = 25,
) -> dict[str, str | int]:
    metadata_rows = fetch_huggingface_rows(
        dataset=metadata_dataset,
        config=config,
        split=split,
        offset=offset,
        length=length,
    )
    review_rows = fetch_huggingface_rows(
        dataset=reviews_dataset,
        config=config,
        split=split,
        offset=offset,
        length=length,
    )
    return write_huggingface_preview(
        metadata_rows=metadata_rows,
        review_rows=review_rows,
        output_dir=output_dir,
    )
