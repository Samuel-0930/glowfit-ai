from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from src.glowfit.schemas import Product, Review


def _sql_literal(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _values(rows: Iterable[tuple[object, ...]]) -> str:
    return ",\n    ".join(
        "(" + ", ".join(_sql_literal(value) for value in row) + ")" for row in rows
    )


def build_supabase_seed_sql(
    products: Iterable[Product], reviews: Iterable[Review], *, replace: bool = False
) -> str:
    product_list = sorted(products, key=lambda product: product.product_id)
    review_list = sorted(reviews, key=lambda review: review.review_id)
    product_ids = {product.product_id for product in product_list}
    invalid_reviews = [
        review.review_id for review in review_list if review.product_id not in product_ids
    ]
    if invalid_reviews:
        message = ", ".join(invalid_reviews)
        raise ValueError(f"Reviews reference products outside the catalog: {message}")

    statements = ["begin;"]
    if replace:
        statements.extend(
            [
                "delete from public.product_tags;",
                "delete from public.reviews;",
                "delete from public.products;",
            ]
        )

    if product_list:
        statements.append(
            "insert into public.products "
            "(product_id, name, category, brand, price_usd, average_rating, review_count) "
            "values\n    "
            + _values(
                (
                    product.product_id,
                    product.name,
                    product.category,
                    product.brand,
                    product.price_usd,
                    product.average_rating,
                    product.review_count,
                )
                for product in product_list
            )
            + "\non conflict (product_id) do update set\n"
            "    name = excluded.name,\n"
            "    category = excluded.category,\n"
            "    brand = excluded.brand,\n"
            "    price_usd = excluded.price_usd,\n"
            "    average_rating = excluded.average_rating,\n"
            "    review_count = excluded.review_count;"
        )

    tags = sorted(
        {
            (product.product_id, attribute[:500])
            for product in product_list
            for attribute in product.attributes
            if attribute.strip()
        }
    )
    if tags:
        statements.append(
            "insert into public.product_tags (product_id, tag) values\n    "
            + _values(tags)
            + "\non conflict (product_id, tag) do nothing;"
        )

    if review_list:
        statements.append(
            "insert into public.reviews "
            "(review_id, user_id, product_id, rating, text, reviewed_on) values\n    "
            + _values(
                (
                    review.review_id,
                    review.user_id,
                    review.product_id,
                    review.rating,
                    review.text,
                    review.timestamp,
                )
                for review in review_list
            )
            + "\non conflict (review_id) do update set\n"
            "    user_id = excluded.user_id,\n"
            "    product_id = excluded.product_id,\n"
            "    rating = excluded.rating,\n"
            "    text = excluded.text,\n"
            "    reviewed_on = excluded.reviewed_on;"
        )
    statements.append("commit;")
    return "\n\n".join(statements) + "\n"


def build_supabase_seed_from_artifact(artifact_dir: Path, *, replace: bool = False) -> str:
    product_rows = json.loads((artifact_dir / "products.json").read_text())
    review_rows = json.loads((artifact_dir / "reviews.json").read_text())
    products = [Product.model_validate(row) for row in product_rows]
    reviews = [Review.model_validate(row) for row in review_rows]
    return build_supabase_seed_sql(products, reviews, replace=replace)
