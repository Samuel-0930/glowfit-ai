from __future__ import annotations

from dataclasses import dataclass

from src.glowfit.nlp import extract_aspects, label_sentiment
from src.glowfit.schemas import EvidenceSnippet, Review


@dataclass(frozen=True)
class EvidenceIndex:
    reviews: tuple[Review, ...]

    @classmethod
    def from_reviews(cls, reviews: list[Review]) -> "EvidenceIndex":
        return cls(reviews=tuple(reviews))

    def search(self, product_id: str, query_terms: list[str], limit: int = 3) -> list[EvidenceSnippet]:
        lowered_terms = [term.lower() for term in query_terms]
        scored: list[tuple[float, Review]] = []

        for review in self.reviews:
            if review.product_id != product_id:
                continue
            text = review.text.lower()
            hits = sum(term in text for term in lowered_terms)
            rating_bonus = max(review.rating - 3, 0) * 0.1
            score = hits + rating_bonus
            if score > 0:
                scored.append((score, review))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            EvidenceSnippet(
                review_id=review.review_id,
                product_id=review.product_id,
                text=review.text,
                sentiment=label_sentiment(review.rating, review.text),
                aspects=extract_aspects(review.text),
                relevance=round(score, 3),
            )
            for score, review in scored[:limit]
        ]
