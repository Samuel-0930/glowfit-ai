from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from src.glowfit.evaluation import evaluate_ranked_product_ids
from src.glowfit.models import _normalize, _tokenize_product
from src.glowfit.schemas import Product, Review


def _review_timestamp(review: Review) -> datetime:
    return datetime.fromisoformat(review.timestamp.replace("Z", "+00:00"))


def _mean_metrics(metric_sets: list[dict[str, float]]) -> dict[str, float]:
    if not metric_sets:
        return {}
    metric_names = metric_sets[0]
    return {
        name: round(sum(metrics[name] for metrics in metric_sets) / len(metric_sets), 4)
        for name in metric_names
    }


def _rank_for_holdout(
    products: list[Product],
    reviews_before_holdout: list[Review],
    user_history: list[Review],
) -> dict[str, list[str]]:
    review_ratings: dict[str, list[int]] = defaultdict(list)
    for review in reviews_before_holdout:
        review_ratings[review.product_id].append(review.rating)

    popularity = dict(
        _normalize(
            {
                product.product_id: float(len(review_ratings[product.product_id]))
                for product in products
            }
        )
    )
    review_average = dict(
        _normalize(
            {
                product.product_id: (
                    sum(review_ratings[product.product_id])
                    / len(review_ratings[product.product_id])
                    if review_ratings[product.product_id]
                    else 0.0
                )
                for product in products
            }
        )
    )
    products_by_id = {product.product_id: product for product in products}
    history_tokens = set().union(
        *(
            _tokenize_product(products_by_id[review.product_id])
            for review in user_history
            if review.product_id in products_by_id and review.rating >= 4
        )
    )
    history_overlap = dict(
        _normalize(
            {
                product.product_id: (
                    len(history_tokens & _tokenize_product(product)) / len(history_tokens)
                    if history_tokens
                    else 0.0
                )
                for product in products
            }
        )
    )
    hybrid = {
        product.product_id: (
            history_overlap[product.product_id] * 0.50
            + review_average[product.product_id] * 0.30
            + popularity[product.product_id] * 0.20
        )
        for product in products
    }

    def ranked_ids(scores: dict[str, float]) -> list[str]:
        return [
            product_id
            for product_id, _score in sorted(
                scores.items(), key=lambda item: (-item[1], item[0])
            )
        ]

    return {
        "popularity": ranked_ids(popularity),
        "review_average": ranked_ids(review_average),
        "history_attribute_overlap": ranked_ids(history_overlap),
        "hybrid": ranked_ids(hybrid),
    }


def build_temporal_user_holdout_report(
    products: list[Product],
    reviews: list[Review],
    relevant_rating_threshold: int,
    k_values: list[int],
    minimum_holdouts: int = 20,
) -> dict[str, object]:
    """Evaluate only positive last interactions using each user's earlier history.

    Product popularity and rating signals are recomputed from reviews earlier than each holdout,
    so a future interaction cannot influence that query's ranking.
    """
    catalog_product_ids = {product.product_id for product in products}
    reviews_by_user: dict[str, list[Review]] = defaultdict(list)
    for review in reviews:
        reviews_by_user[review.user_id].append(review)

    evaluations: dict[str, list[dict[str, float]]] = defaultdict(list)
    eligible_users = 0
    skipped_users = 0
    for user_reviews in reviews_by_user.values():
        ordered_reviews = sorted(
            user_reviews,
            key=lambda review: (_review_timestamp(review), review.review_id),
        )
        if len(ordered_reviews) < 2:
            skipped_users += 1
            continue
        held_out = ordered_reviews[-1]
        history = ordered_reviews[:-1]
        if (
            held_out.rating < relevant_rating_threshold
            or held_out.product_id not in catalog_product_ids
            or not any(
                review.product_id in catalog_product_ids
                and review.rating >= relevant_rating_threshold
                for review in history
            )
        ):
            skipped_users += 1
            continue

        eligible_users += 1
        reviews_before_holdout = [
            review for review in reviews if _review_timestamp(review) < _review_timestamp(held_out)
        ]
        for model_name, ranked_product_ids in _rank_for_holdout(
            products, reviews_before_holdout, history
        ).items():
            evaluations[model_name].append(
                evaluate_ranked_product_ids(
                    ranked_product_ids, [held_out.product_id], k_values
                )
            )

    warnings: list[str] = []
    if eligible_users < minimum_holdouts:
        warnings.append(
            f"Only {eligible_users} eligible user holdouts; at least {minimum_holdouts} "
            "are required for comparison."
        )
    if eligible_users == 0:
        warnings.append(
            "No user has a positive last interaction and an earlier positive history "
            "in the catalog."
        )

    return {
        "protocol": "per-user last positive interaction holdout with time-bounded ranking signals",
        "eligible_user_count": eligible_users,
        "skipped_user_count": skipped_users,
        "minimum_holdouts": minimum_holdouts,
        "comparative_ready": not warnings,
        "warnings": warnings,
        "models": {
            model_name: {"metrics": _mean_metrics(metric_sets)}
            for model_name, metric_sets in evaluations.items()
        },
    }
