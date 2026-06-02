from src.glowfit.nlp import extract_aspects, label_sentiment, summarize_product_reviews
from src.glowfit.schemas import Review


def test_extract_aspects_detects_beauty_keywords():
    text = "Light gel texture, fragrance free, and calming for dry skin."

    assert extract_aspects(text) == ["texture", "fragrance", "dry skin", "calming"]


def test_label_sentiment_uses_rating_and_text_cues():
    assert label_sentiment(5, "excellent and gentle") == "positive"
    assert label_sentiment(2, "sticky and irritating") == "negative"
    assert label_sentiment(3, "fine but not special") == "mixed"


def test_summarize_product_reviews_aggregates_aspects():
    reviews = [
        Review(
            review_id="r1",
            user_id="u1",
            product_id="p1",
            rating=5,
            text="Light and gentle texture.",
            timestamp="2025-01-01",
        ),
        Review(
            review_id="r2",
            user_id="u2",
            product_id="p1",
            rating=4,
            text="Fragrance free and calming.",
            timestamp="2025-01-02",
        ),
    ]

    summary = summarize_product_reviews(reviews)

    assert summary["product_id"] == "p1"
    assert summary["average_rating"] == 4.5
    assert "texture" in summary["top_aspects"]
    assert "fragrance" in summary["top_aspects"]
