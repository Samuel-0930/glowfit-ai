from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews


SAMPLE_DIR = Path("sample_data")


def test_load_products_maps_product_records():
    products = load_products(SAMPLE_DIR / "products.json")

    assert len(products) == 3
    assert products[0].product_id == "p_glow_gel"
    assert "fragrance free" in products[0].attributes


def test_load_reviews_maps_review_records():
    reviews = load_reviews(SAMPLE_DIR / "reviews.json")

    assert len(reviews) == 5
    assert reviews[0].rating == 5
    assert reviews[0].product_id == "p_glow_gel"


def test_load_preferences_maps_user_intake():
    preferences = load_preferences(SAMPLE_DIR / "preferences.json")

    assert preferences.skin_type == "dry"
    assert preferences.fragrance_sensitivity == "high"
    assert "barrier care" in preferences.concerns
