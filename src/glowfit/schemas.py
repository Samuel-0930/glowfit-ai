from __future__ import annotations

from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: str
    name: str
    category: str
    brand: str
    price_usd: float
    average_rating: float
    review_count: int
    attributes: list[str] = Field(default_factory=list)


class Review(BaseModel):
    review_id: str
    user_id: str
    product_id: str
    rating: int
    text: str
    timestamp: str


class UserPreferences(BaseModel):
    skin_type: str
    concerns: list[str] = Field(default_factory=list)
    texture: str
    fragrance_sensitivity: str
    budget_max_usd: float
    avoid: list[str] = Field(default_factory=list)


class EvidenceSnippet(BaseModel):
    review_id: str
    product_id: str
    text: str
    sentiment: str
    aspects: list[str]
    relevance: float


class Recommendation(BaseModel):
    product: Product
    fit_score: float
    confidence: float
    reasons: list[str]
    cautions: list[str]
    evidence: list[EvidenceSnippet]
    model_scores: dict[str, float]
