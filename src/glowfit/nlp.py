from __future__ import annotations

from collections import Counter

from src.glowfit.schemas import Review

ASPECT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "texture": ("texture", "gel", "watery", "light", "sticky", "matte"),
    "fragrance": ("fragrance", "scent", "scented", "fragrance free"),
    "dry skin": ("dry skin", "dry patches", "hydrating", "moisturizing"),
    "oily skin": ("oily skin", "matte", "shine"),
    "sensitive skin": ("sensitive", "sting", "irritating", "gentle"),
    "calming": ("calm", "calming", "redness", "cica"),
    "finish": ("finish", "white cast", "under makeup"),
}

POSITIVE_CUES = ("excellent", "great", "gentle", "calm", "helped", "moisturizing", "absorbs")
NEGATIVE_CUES = ("sticky", "irritating", "sting", "not hydrating", "noticeable", "dry patches")


def extract_aspects(text: str) -> list[str]:
    lowered = text.lower()
    aspects: list[str] = []
    for aspect, keywords in ASPECT_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            aspects.append(aspect)
    return aspects


def label_sentiment(rating: int, text: str) -> str:
    lowered = text.lower()
    positive_hits = sum(cue in lowered for cue in POSITIVE_CUES)
    negative_hits = sum(cue in lowered for cue in NEGATIVE_CUES)
    if rating >= 4 and positive_hits >= negative_hits:
        return "positive"
    if rating <= 2 or negative_hits > positive_hits + 1:
        return "negative"
    return "mixed"


def summarize_product_reviews(reviews: list[Review]) -> dict[str, object]:
    if not reviews:
        raise ValueError("Cannot summarize an empty review list")

    aspect_counts: Counter[str] = Counter()
    sentiment_counts: Counter[str] = Counter()
    for review in reviews:
        aspect_counts.update(extract_aspects(review.text))
        sentiment_counts.update([label_sentiment(review.rating, review.text)])

    average_rating = sum(review.rating for review in reviews) / len(reviews)
    return {
        "product_id": reviews[0].product_id,
        "review_count": len(reviews),
        "average_rating": round(average_rating, 2),
        "top_aspects": [aspect for aspect, _ in aspect_counts.most_common(5)],
        "sentiment_counts": dict(sentiment_counts),
    }
