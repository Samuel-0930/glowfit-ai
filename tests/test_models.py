from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.models import (
    CollaborativeFilteringRecommender,
    ContentBasedRecommender,
    PopularityRecommender,
    RatingRecommender,
    TwoTowerRetrieval,
)
from src.glowfit.schemas import Product, UserPreferences


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


def test_avoid_terms_do_not_increase_positive_match_scores():
    products = [
        Product(
            product_id="safe",
            name="Plain Serum",
            category="serum",
            brand="A",
            price_usd=10,
            average_rating=4,
            review_count=10,
            attributes=["fragrance free"],
        ),
        Product(
            product_id="avoid",
            name="Scent Serum",
            category="serum",
            brand="B",
            price_usd=10,
            average_rating=4,
            review_count=10,
            attributes=["strong scent"],
        ),
    ]
    preferences = UserPreferences(
        skin_type="dry",
        concerns=[],
        texture="light",
        fragrance_sensitivity="high",
        budget_max_usd=20,
        avoid=["strong scent"],
    )

    content_scores = dict(ContentBasedRecommender().score(products, preferences))
    similarity_scores = dict(TwoTowerRetrieval(embedding_dim=64).score(products, preferences))

    assert content_scores["safe"] > content_scores["avoid"]
    assert similarity_scores["safe"] > similarity_scores["avoid"]
