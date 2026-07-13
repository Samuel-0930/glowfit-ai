from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

SkinType = Literal["dry", "oily", "combination", "sensitive"]
Texture = Literal["light", "watery", "gel", "cream", "lotion"]
FragranceSensitivity = Literal["low", "medium", "high"]
PreferenceTerm = Annotated[str, Field(min_length=1, max_length=50)]
ProductId = Annotated[str, Field(min_length=1, max_length=100)]


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
    skin_type: SkinType
    concerns: list[PreferenceTerm] = Field(default_factory=list, max_length=10)
    texture: Texture
    fragrance_sensitivity: FragranceSensitivity
    budget_max_usd: float = Field(ge=0, le=500)
    avoid: list[PreferenceTerm] = Field(default_factory=list, max_length=10)


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
