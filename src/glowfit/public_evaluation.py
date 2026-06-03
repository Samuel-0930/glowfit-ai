from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.glowfit.data import load_products, load_reviews
from src.glowfit.evaluation import evaluate_ranked_product_ids
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.models import (
    CollaborativeFilteringRecommender,
    ContentBasedRecommender,
    PopularityRecommender,
    RatingRecommender,
    TwoTowerRetrieval,
)
from src.glowfit.ranking import recommend
from src.glowfit.schemas import Product, Review, UserPreferences


def default_public_preferences() -> UserPreferences:
    return UserPreferences(
        skin_type="dry",
        concerns=["redness", "barrier care"],
        texture="light",
        fragrance_sensitivity="high",
        budget_max_usd=25,
        avoid=["strong scent", "sticky finish"],
    )


def _relevant_product_ids(reviews: list[Review], relevant_rating_threshold: int) -> list[str]:
    return sorted(
        {
            review.product_id
            for review in reviews
            if review.rating >= relevant_rating_threshold and review.product_id
        }
    )


def _ranked_ids_from_scores(scores: list[tuple[str, float]]) -> list[str]:
    return [product_id for product_id, _score in scores]


def _model_rankings(
    products: list[Product],
    reviews: list[Review],
    preferences: UserPreferences,
    evidence_index: EvidenceIndex,
) -> dict[str, list[str]]:
    return {
        "popularity": _ranked_ids_from_scores(PopularityRecommender().score(products)),
        "rating": _ranked_ids_from_scores(RatingRecommender().score(products)),
        "collaborative": _ranked_ids_from_scores(
            CollaborativeFilteringRecommender().score(products, reviews)
        ),
        "content": _ranked_ids_from_scores(ContentBasedRecommender().score(products, preferences)),
        "two_tower": _ranked_ids_from_scores(TwoTowerRetrieval().score(products, preferences)),
        "hybrid": [
            item.product.product_id
            for item in recommend(products, preferences, evidence_index, limit=len(products))
        ],
    }


def build_public_artifact_evaluation_report(
    artifact_dir: Path,
    relevant_rating_threshold: int = 4,
    k_values: list[int] | None = None,
    preferences: UserPreferences | None = None,
) -> dict[str, Any]:
    resolved_k_values = k_values or [1, 3, 5]
    resolved_preferences = preferences or default_public_preferences()
    products = load_products(artifact_dir / "products.json")
    reviews = load_reviews(artifact_dir / "reviews.json")
    evidence_index = EvidenceIndex.from_reviews(reviews)
    relevant_product_ids = _relevant_product_ids(reviews, relevant_rating_threshold)

    models: dict[str, dict[str, Any]] = {}
    for model_name, ranked_product_ids in _model_rankings(
        products=products,
        reviews=reviews,
        preferences=resolved_preferences,
        evidence_index=evidence_index,
    ).items():
        models[model_name] = {
            "ranked_product_ids": ranked_product_ids,
            "metrics": evaluate_ranked_product_ids(
                ranked_product_ids=ranked_product_ids,
                relevant_product_ids=relevant_product_ids,
                k_values=resolved_k_values,
            ),
        }

    return {
        "artifact_dir": str(artifact_dir),
        "product_count": len(products),
        "review_count": len(reviews),
        "relevance_rule": f"review_rating >= {relevant_rating_threshold}",
        "relevant_product_ids": relevant_product_ids,
        "k_values": resolved_k_values,
        "profile": resolved_preferences.model_dump(),
        "models": models,
    }


def write_public_artifact_evaluation_report(
    artifact_dir: Path,
    output_path: Path,
    relevant_rating_threshold: int = 4,
    k_values: list[int] | None = None,
) -> dict[str, Any]:
    report = build_public_artifact_evaluation_report(
        artifact_dir=artifact_dir,
        relevant_rating_threshold=relevant_rating_threshold,
        k_values=k_values,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
