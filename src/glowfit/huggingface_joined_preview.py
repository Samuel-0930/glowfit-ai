from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen as default_urlopen

from src.glowfit.huggingface_preview import (
    DATASET_VIEWER_BASE_URL,
    _metadata_row_to_product,
    _review_row_to_review,
    fetch_huggingface_rows,
)

FetchRows = Callable[[str, str, str, int, int], list[dict[str, Any]]]
SearchRows = Callable[[str, str, str, str, int, int], list[dict[str, Any]]]


def fetch_huggingface_search_rows(
    dataset: str,
    config: str,
    split: str,
    query: str,
    offset: int,
    length: int,
    urlopen: Callable[..., Any] = default_urlopen,
    timeout: int = 20,
) -> list[dict[str, Any]]:
    query_string = urlencode(
        {
            "dataset": dataset,
            "config": config,
            "split": split,
            "query": query,
            "offset": offset,
            "length": length,
        }
    )
    url = f"{DATASET_VIEWER_BASE_URL}/search?{query_string}"
    try:
        with urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, TimeoutError, URLError):
        return []
    return [item["row"] for item in payload.get("rows", [])]


def _row_asin(row: dict[str, Any]) -> str:
    return str(row.get("asin") or row.get("parent_asin") or "").strip()


def _first_exact_metadata_match(
    metadata_rows: list[dict[str, Any]],
    asin: str,
) -> dict[str, Any] | None:
    for row in metadata_rows:
        row_asin = _row_asin(row)
        if row_asin == asin:
            return row
    return None


def _write_joined_preview(
    product_rows: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    output_dir: Path,
    summary: dict[str, str | int],
) -> dict[str, str | int]:
    products = [_metadata_row_to_product(row) for row in product_rows]
    reviews = [_review_row_to_review(row, index) for index, row in enumerate(review_rows, start=1)]

    output_dir.mkdir(parents=True, exist_ok=True)
    products_path = output_dir / "products.json"
    reviews_path = output_dir / "reviews.json"
    summary_path = output_dir / "summary.json"
    products_path.write_text(
        json.dumps([product.model_dump() for product in products], indent=2),
        encoding="utf-8",
    )
    reviews_path.write_text(
        json.dumps([review.model_dump() for review in reviews], indent=2),
        encoding="utf-8",
    )
    result = {
        **summary,
        "products_written": len(products),
        "reviews_written": len(reviews),
        "products_path": str(products_path),
        "reviews_path": str(reviews_path),
        "summary_path": str(summary_path),
    }
    summary_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def fetch_and_write_joined_huggingface_preview(
    output_dir: Path,
    metadata_dataset: str = "smartcat/Amazon_All_Beauty_2023",
    reviews_dataset: str = "jhan21/amazon-beauty-reviews-dataset",
    config: str = "default",
    split: str = "train",
    review_offset: int = 0,
    target_matches: int = 25,
    review_page_size: int = 25,
    max_review_rows: int = 250,
    metadata_search_length: int = 5,
    fetch_rows: FetchRows = fetch_huggingface_rows,
    search_rows: SearchRows = fetch_huggingface_search_rows,
) -> dict[str, str | int]:
    matched_product_rows: list[dict[str, Any]] = []
    matched_review_rows: list[dict[str, Any]] = []
    seen_asins: set[str] = set()
    review_rows_scanned = 0
    metadata_searches = 0

    while review_rows_scanned < max_review_rows and len(matched_review_rows) < target_matches:
        page_offset = review_offset + review_rows_scanned
        page_length = min(review_page_size, max_review_rows - review_rows_scanned)
        review_page = fetch_rows(reviews_dataset, config, split, page_offset, page_length)
        if not review_page:
            break

        for review_row in review_page:
            review_rows_scanned += 1
            asin = _row_asin(review_row)
            if not asin or asin in seen_asins:
                continue

            metadata_searches += 1
            metadata_rows = search_rows(
                metadata_dataset,
                config,
                split,
                asin,
                0,
                metadata_search_length,
            )
            metadata_row = _first_exact_metadata_match(metadata_rows, asin)
            if metadata_row is None:
                continue

            seen_asins.add(asin)
            matched_product_rows.append(metadata_row)
            matched_review_rows.append(review_row)
            if len(matched_review_rows) >= target_matches:
                break

    return _write_joined_preview(
        product_rows=matched_product_rows,
        review_rows=matched_review_rows,
        output_dir=output_dir,
        summary={
            "target_matches": target_matches,
            "review_rows_scanned": review_rows_scanned,
            "metadata_searches": metadata_searches,
        },
    )
