from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from src.glowfit.data import load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend
from src.glowfit.schemas import Recommendation, UserPreferences


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]


class ReportResponse(BaseModel):
    summary: str
    recommendations: list[Recommendation]
    generation_mode: str


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


@app.post("/report", response_model=ReportResponse)
def report(preferences: UserPreferences) -> ReportResponse:
    recommendations = recommend(PRODUCTS, preferences, EVIDENCE, limit=3)
    top = recommendations[0]
    summary = (
        f"{top.product.name} is the strongest match because it aligns with "
        f"{', '.join(top.reasons)} and has review evidence for the requested profile."
    )
    return ReportResponse(
        summary=summary,
        recommendations=recommendations,
        generation_mode="deterministic",
    )


@app.post("/compare")
def compare(product_ids: list[str]) -> dict[str, object]:
    selected = [product for product in PRODUCTS if product.product_id in product_ids]
    return {"products": selected}
