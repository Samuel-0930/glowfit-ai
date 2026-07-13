from __future__ import annotations

from src.glowfit.evidence import EvidenceIndex
from src.glowfit.models import (
    ContentBasedRecommender,
    HashVectorSimilarityRecommender,
    PopularityRecommender,
    RatingRecommender,
    ReviewAverageRecommender,
)
from src.glowfit.schemas import Product, Recommendation, UserPreferences


def _as_score_map(ranked: list[tuple[str, float]]) -> dict[str, float]:
    return {product_id: score for product_id, score in ranked}


def _reason_terms(preferences: UserPreferences) -> list[str]:
    terms = [preferences.skin_type, preferences.texture, *preferences.concerns]
    if preferences.fragrance_sensitivity == "high":
        terms.append("fragrance")
    return terms


def recommend(
    products: list[Product],
    preferences: UserPreferences,
    evidence_index: EvidenceIndex,
    limit: int = 3,
) -> list[Recommendation]:
    popularity = _as_score_map(PopularityRecommender().score(products))
    rating = _as_score_map(RatingRecommender().score(products))
    review_average = _as_score_map(
        ReviewAverageRecommender().score(products, evidence_index.reviews)
    )
    content = _as_score_map(ContentBasedRecommender().score(products, preferences))
    hash_similarity = _as_score_map(
        HashVectorSimilarityRecommender().score(products, preferences)
    )
    query_terms = _reason_terms(preferences)

    recommendations: list[Recommendation] = []
    for product in products:
        snippets = evidence_index.search(product.product_id, query_terms=query_terms, limit=3)
        evidence_bonus = min(len(snippets) * 0.05, 0.15)
        score = (
            content.get(product.product_id, 0) * 0.40
            + hash_similarity.get(product.product_id, 0) * 0.30
            + review_average.get(product.product_id, 0) * 0.15
            + popularity.get(product.product_id, 0) * 0.10
            + evidence_bonus
        )
        cautions = [
            avoid
            for avoid in preferences.avoid
            if any(avoid.lower() in attribute.lower() for attribute in product.attributes)
        ]
        reasons = [
            attribute
            for attribute in product.attributes
            if any(term.lower() in attribute.lower() for term in query_terms)
        ][:3]
        recommendations.append(
            Recommendation(
                product=product,
                fit_score=round(min(score, 1.0), 4),
                evidence_strength=round(min(0.55 + len(snippets) * 0.1, 0.95), 2),
                reasons=reasons or product.attributes[:2],
                cautions=cautions,
                evidence=snippets,
                model_scores={
                    "popularity": popularity.get(product.product_id, 0),
                    "rating": rating.get(product.product_id, 0),
                    "review_average": review_average.get(product.product_id, 0),
                    "content": content.get(product.product_id, 0),
                    "hash_similarity": hash_similarity.get(product.product_id, 0),
                },
            )
        )

    recommendations.sort(key=lambda item: item.fit_score, reverse=True)
    return recommendations[:limit]
