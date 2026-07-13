from __future__ import annotations

import hashlib
import math
from collections import defaultdict

import numpy as np

from src.glowfit.schemas import Product, Review, UserPreferences


def _normalize(scores: dict[str, float]) -> list[tuple[str, float]]:
    if not scores:
        return []
    values = np.array(list(scores.values()), dtype=float)
    minimum = float(values.min())
    maximum = float(values.max())
    if math.isclose(maximum, minimum):
        return sorted(((key, 1.0) for key in scores), key=lambda item: item[0])
    normalized = {
        key: round((value - minimum) / (maximum - minimum), 4) for key, value in scores.items()
    }
    return sorted(normalized.items(), key=lambda item: item[1], reverse=True)


def _tokenize_product(product: Product) -> set[str]:
    tokens = set(product.category.lower().split())
    for attribute in product.attributes:
        tokens.update(attribute.lower().split())
        tokens.add(attribute.lower())
    return tokens


def _tokenize_preferences(preferences: UserPreferences) -> set[str]:
    tokens = {preferences.skin_type.lower(), preferences.texture.lower()}
    for concern in preferences.concerns:
        tokens.update(concern.lower().split())
        tokens.add(concern.lower())
    if preferences.fragrance_sensitivity == "high":
        tokens.add("fragrance free")
    return tokens


class PopularityRecommender:
    def score(self, products: list[Product]) -> list[tuple[str, float]]:
        return _normalize({product.product_id: float(product.review_count) for product in products})


class RatingRecommender:
    def score(self, products: list[Product]) -> list[tuple[str, float]]:
        return _normalize({product.product_id: product.average_rating for product in products})


class ContentBasedRecommender:
    def score(
        self, products: list[Product], preferences: UserPreferences
    ) -> list[tuple[str, float]]:
        preference_tokens = _tokenize_preferences(preferences)
        scores: dict[str, float] = {}
        for product in products:
            product_tokens = _tokenize_product(product)
            overlap = len(preference_tokens & product_tokens)
            avoid_hits = sum(term.lower() in product_tokens for term in preferences.avoid)
            budget_bonus = 1.0 if product.price_usd <= preferences.budget_max_usd else -1.0
            scores[product.product_id] = overlap + budget_bonus - avoid_hits
        return _normalize(scores)


class CollaborativeFilteringRecommender:
    def score(self, products: list[Product], reviews: list[Review]) -> list[tuple[str, float]]:
        rating_totals: dict[str, list[int]] = defaultdict(list)
        for review in reviews:
            rating_totals[review.product_id].append(review.rating)
        scores = {
            product.product_id: (
                sum(rating_totals[product.product_id]) / len(rating_totals[product.product_id])
                if rating_totals[product.product_id]
                else product.average_rating
            )
            for product in products
        }
        return _normalize(scores)


class TwoTowerRetrieval:
    def __init__(self, embedding_dim: int = 16) -> None:
        self.embedding_dim = embedding_dim

    def _embed_text(self, text: str) -> np.ndarray:
        vector = np.zeros(self.embedding_dim, dtype=float)
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % self.embedding_dim
            vector[index] += 1.0
        norm = np.linalg.norm(vector)
        return vector if norm == 0 else vector / norm

    def score(
        self, products: list[Product], preferences: UserPreferences
    ) -> list[tuple[str, float]]:
        preference_text = " ".join(sorted(_tokenize_preferences(preferences)))
        user_vector = self._embed_text(preference_text)
        scores: dict[str, float] = {}
        for product in products:
            product_text = " ".join([product.name, product.category, *product.attributes])
            product_vector = self._embed_text(product_text)
            cosine = float(np.dot(user_vector, product_vector))
            scores[product.product_id] = cosine
        return _normalize(scores)
