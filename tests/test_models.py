from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.models import (
    CollaborativeFilteringRecommender,
    ContentBasedRecommender,
    PopularityRecommender,
    RatingRecommender,
    TwoTowerRetrieval,
)


def test_popularity_recommender_orders_by_review_count():
    products = load_products(Path("sample_data/products.json"))
    ranked = PopularityRecommender().score(products)

    assert ranked[0][0] == "p_glow_gel"
    assert ranked[0][1] > ranked[-1][1]


def test_rating_recommender_orders_by_average_rating():
    products = load_products(Path("sample_data/products.json"))
    ranked = RatingRecommender().score(products)

    assert ranked[0][0] == "p_glow_gel"


def test_content_based_recommender_rewards_matching_preferences():
    products = load_products(Path("sample_data/products.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))

    ranked = ContentBasedRecommender().score(products, preferences)

    assert ranked[0][0] == "p_glow_gel"


def test_collaborative_filtering_recommender_uses_rating_history():
    products = load_products(Path("sample_data/products.json"))
    reviews = load_reviews(Path("sample_data/reviews.json"))

    ranked = CollaborativeFilteringRecommender().score(products, reviews)

    assert ranked[0][0] == "p_glow_gel"
    assert all(0 <= score <= 1 for _, score in ranked)


def test_two_tower_retrieval_returns_normalized_scores():
    products = load_products(Path("sample_data/products.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))

    ranked = TwoTowerRetrieval(embedding_dim=8).score(products, preferences)

    assert len(ranked) == 3
    assert all(0 <= score <= 1 for _, score in ranked)
