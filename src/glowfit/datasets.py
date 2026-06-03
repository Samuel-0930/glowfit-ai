from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from src.glowfit.schemas import Product, Review


def _clean_price(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    if isinstance(value, int | float):
        return float(value)
    match = re.search(r"\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(match.group(0)) if match else 0.0


def _category_from_record(record: dict[str, Any]) -> str:
    categories = record.get("categories") or record.get("category") or []
    if isinstance(categories, list) and categories:
        last_path = categories[-1]
        if isinstance(last_path, list) and last_path:
            return str(last_path[-1]).strip().lower()
        return str(last_path).strip().lower()
    return "beauty"


def _attributes_from_record(record: dict[str, Any]) -> list[str]:
    raw_features = record.get("features") or record.get("description") or []
    if isinstance(raw_features, str):
        raw_features = [raw_features]
    return [str(feature).strip().lower() for feature in raw_features if str(feature).strip()]


def parse_amazon_metadata_record(record: dict[str, Any]) -> Product:
    return Product(
        product_id=str(record["asin"]),
        name=str(record.get("title") or record.get("name") or record["asin"]),
        category=_category_from_record(record),
        brand=str(record.get("brand") or "Unknown"),
        price_usd=_clean_price(record.get("price")),
        average_rating=float(record.get("average_rating") or record.get("rating") or 0.0),
        review_count=int(record.get("rating_number") or record.get("review_count") or 0),
        attributes=_attributes_from_record(record),
    )


def parse_amazon_review_record(record: dict[str, Any], fallback_index: int) -> Review:
    product_id = str(record["asin"])
    unix_time = int(record.get("unixReviewTime") or 0)
    timestamp = (
        datetime.fromtimestamp(unix_time, tz=UTC).date().isoformat() if unix_time else "1970-01-01"
    )
    return Review(
        review_id=str(record.get("reviewerID") and record.get("reviewTime") or "")
        or f"amazon_{product_id}_{fallback_index}",
        user_id=str(record.get("reviewerID") or "unknown"),
        product_id=product_id,
        rating=int(record.get("overall") or record.get("rating") or 0),
        text=str(record.get("reviewText") or record.get("summary") or ""),
        timestamp=timestamp,
    )
