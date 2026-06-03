from __future__ import annotations

from pathlib import Path
from typing import Any

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.evaluation import evaluate_ranked_product_ids
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend


def build_sample_evaluation_report(sample_data_dir: Path) -> dict[str, Any]:
    products = load_products(sample_data_dir / "products.json")
    reviews = load_reviews(sample_data_dir / "reviews.json")
    preferences = load_preferences(sample_data_dir / "preferences.json")
    evidence_index = EvidenceIndex.from_reviews(reviews)
    recommendations = recommend(products, preferences, evidence_index, limit=len(products))
    ranked_product_ids = [item.product.product_id for item in recommendations]

    relevant_product_ids = ["p_glow_gel", "p_calm_ampoule"]
    return {
        "profile": "default_dry_sensitive_profile",
        "relevant_product_ids": relevant_product_ids,
        "ranked_product_ids": ranked_product_ids,
        "metrics": evaluate_ranked_product_ids(
            ranked_product_ids=ranked_product_ids,
            relevant_product_ids=relevant_product_ids,
            k_values=[1, 3],
        ),
    }
