from __future__ import annotations

import json

from src.glowfit.huggingface_hub_catalog import (
    collect_matching_reviews,
    select_hub_products,
    write_hub_catalog,
)


def test_select_hub_products_keeps_high_review_skincare_products() -> None:
    products = select_hub_products(
        [
            {
                "parent_asin": "low",
                "title": "Daily face moisturizer",
                "rating_number": 3,
                "average_rating": 4.8,
            },
            {
                "parent_asin": "high",
                "title": "Hydrating skincare serum",
                "rating_number": 20,
                "average_rating": 4.2,
            },
            {
                "parent_asin": "hair",
                "title": "Hydrating hair conditioner for sensitive scalp",
                "rating_number": 50,
            },
            {"parent_asin": "skip", "title": "Tattoo machine", "rating_number": 100},
        ],
        max_products=2,
    )

    assert [product.product_id for product in products] == ["high", "low"]


def test_collect_matching_reviews_accepts_hub_csv_shape() -> None:
    reviews = collect_matching_reviews(
        [
            {
                "asin": "variant-1",
                "parent_asin": "product-1",
                "user_id": "user-1",
                "rating": "5",
                "text": "Absorbs quickly and feels light.",
                "timestamp": "2024-01-02 10:00:00",
            },
            {
                "parent_asin": "product-1",
                "user_id": "user-2",
                "rating": "4",
                "text": "Good for sensitive skin.",
                "timestamp": "2024-01-03 10:00:00",
            },
        ],
        product_ids={"product-1"},
        min_reviews_per_product=2,
        max_reviews_per_product=3,
    )

    assert len(reviews) == 2
    assert reviews[0].product_id == "product-1"
    assert reviews[0].timestamp == "2024-01-02"


def test_write_hub_catalog_excludes_products_without_required_review_history(tmp_path) -> None:
    summary = write_hub_catalog(
        metadata_rows=[
            {"parent_asin": "ready", "title": "Hydrating face serum", "rating_number": 10},
            {"parent_asin": "missing", "title": "Daily skincare moisturizer", "rating_number": 9},
        ],
        review_rows=[
            {"parent_asin": "ready", "rating": "5", "text": "Light and hydrating."},
            {"parent_asin": "ready", "rating": "4", "text": "No strong fragrance."},
        ],
        output_dir=tmp_path,
        max_products=2,
        min_reviews_per_product=2,
        max_reviews_per_product=3,
    )

    assert summary["products_written"] == 1
    assert summary["reviews_written"] == 2
    assert json.loads((tmp_path / "products.json").read_text())[0]["product_id"] == "ready"


def test_write_hub_catalog_selects_products_seen_in_review_stream(tmp_path) -> None:
    summary = write_hub_catalog(
        metadata_rows=[
            {"parent_asin": "late", "title": "Hydrating face serum", "rating_number": 99},
            {"parent_asin": "early", "title": "Daily skincare moisturizer", "rating_number": 1},
        ],
        review_rows=[
            {"parent_asin": "early", "rating": "5", "text": "Hydrating."},
            {"parent_asin": "early", "rating": "4", "text": "Lightweight."},
        ],
        output_dir=tmp_path,
        max_products=1,
        min_reviews_per_product=2,
        max_reviews_per_product=3,
    )

    assert summary["products_written"] == 1
    assert json.loads((tmp_path / "products.json").read_text())[0]["product_id"] == "early"
