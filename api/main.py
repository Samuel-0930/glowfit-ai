from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.glowfit.data import load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend
from src.glowfit.schemas import Recommendation, UserPreferences


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]


class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    limit: int = Field(default=3, ge=1, le=10)


class RecommendationMetadata(BaseModel):
    data_source: str
    product_count: int
    review_count: int
    requested_limit: int
    returned_count: int
    top_product_id: str | None


class ReportResponse(BaseModel):
    summary: str
    recommendations: list[Recommendation]
    generation_mode: str


class RecommendationsResponse(ReportResponse):
    metadata: RecommendationMetadata


PRODUCTS = load_products(Path("sample_data/products.json"))
REVIEWS = load_reviews(Path("sample_data/reviews.json"))
EVIDENCE = EvidenceIndex.from_reviews(REVIEWS)

app = FastAPI(title="GlowFit AI API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "product_count": len(PRODUCTS),
        "review_count": len(REVIEWS),
    }


@app.get("/products")
def products() -> dict[str, object]:
    return {"products": PRODUCTS}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_products(preferences: UserPreferences) -> RecommendationResponse:
    return RecommendationResponse(
        recommendations=recommend(PRODUCTS, preferences, EVIDENCE, limit=3)
    )


def _build_summary(recommendations: list[Recommendation]) -> str:
    if not recommendations:
        return "No recommendations were generated for the current profile."

    top = recommendations[0]
    reason_text = ", ".join(top.reasons[:3]) or "the selected profile signals"
    return (
        f"{top.product.name} is the strongest match because it aligns with "
        f"{reason_text} and has review evidence for the requested profile."
    )


@app.post("/recommendations", response_model=RecommendationsResponse)
def create_recommendations(request: RecommendationRequest) -> RecommendationsResponse:
    recommendations = recommend(PRODUCTS, request.preferences, EVIDENCE, limit=request.limit)
    return RecommendationsResponse(
        summary=_build_summary(recommendations),
        recommendations=recommendations,
        generation_mode="api-hybrid-ranking",
        metadata=RecommendationMetadata(
            data_source="sample_data",
            product_count=len(PRODUCTS),
            review_count=len(REVIEWS),
            requested_limit=request.limit,
            returned_count=len(recommendations),
            top_product_id=recommendations[0].product.product_id if recommendations else None,
        ),
    )


@app.post("/report", response_model=ReportResponse)
def report(preferences: UserPreferences) -> ReportResponse:
    recommendations = recommend(PRODUCTS, preferences, EVIDENCE, limit=3)
    return ReportResponse(
        summary=_build_summary(recommendations),
        recommendations=recommendations,
        generation_mode="deterministic",
    )


@app.post("/compare")
def compare(product_ids: list[str]) -> dict[str, object]:
    selected = [product for product in PRODUCTS if product.product_id in product_ids]
    return {"products": selected}
