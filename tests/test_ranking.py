from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend


def test_recommend_returns_ranked_recommendations_with_evidence():
    products = load_products(Path("sample_data/products.json"))
    reviews = load_reviews(Path("sample_data/reviews.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))
    evidence_index = EvidenceIndex.from_reviews(reviews)

    recommendations = recommend(products, preferences, evidence_index, limit=2)

    assert len(recommendations) == 2
    assert recommendations[0].product.product_id == "p_glow_gel"
    assert recommendations[0].fit_score > recommendations[1].fit_score
    assert recommendations[0].evidence
    assert "content" in recommendations[0].model_scores
    assert "collaborative" in recommendations[0].model_scores
    assert "two_tower" in recommendations[0].model_scores
