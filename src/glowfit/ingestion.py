from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from src.glowfit.datasets import parse_amazon_metadata_record, parse_amazon_review_record
from src.glowfit.schemas import Product, Review


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if not isinstance(payload, dict):
                raise ValueError(f"Expected object on line {line_number} of {path}")
            yield payload


def _is_beauty_record(record: dict[str, Any]) -> bool:
    categories = record.get("categories") or record.get("category") or []
    category_text = json.dumps(categories).lower()
    title = str(record.get("title") or "").lower()
    beauty_terms = ("beauty", "skin care", "skincare", "moisturizer", "serum", "sunscreen")
    return any(term in category_text or term in title for term in beauty_terms)


def ingest_amazon_beauty_jsonl(
    metadata_path: Path,
    reviews_path: Path,
    output_dir: Path,
    limit: int | None = None,
) -> dict[str, str | int]:
    products: list[Product] = []
    product_ids: set[str] = set()
    for record in _iter_jsonl(metadata_path):
        if not _is_beauty_record(record):
            continue
        product = parse_amazon_metadata_record(record)
        products.append(product)
        product_ids.add(product.product_id)
        if limit is not None and len(products) >= limit:
            break

    reviews: list[Review] = []
    for index, record in enumerate(_iter_jsonl(reviews_path), start=1):
        if str(record.get("asin")) not in product_ids:
            continue
        reviews.append(parse_amazon_review_record(record, fallback_index=index))
        if limit is not None and len(reviews) >= limit:
            break

    output_dir.mkdir(parents=True, exist_ok=True)
    products_path = output_dir / "products.json"
    reviews_path_out = output_dir / "reviews.json"
    products_path.write_text(
        json.dumps([product.model_dump() for product in products], indent=2),
        encoding="utf-8",
    )
    reviews_path_out.write_text(
        json.dumps([review.model_dump() for review in reviews], indent=2),
        encoding="utf-8",
    )

    return {
        "products_written": len(products),
        "reviews_written": len(reviews),
        "products_path": str(products_path),
        "reviews_path": str(reviews_path_out),
    }
