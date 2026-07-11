from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.glowfit.catalog import Catalog, get_catalog_repository
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


app = FastAPI(title="GlowFit AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("GLOWFIT_CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


def _catalog() -> Catalog:
    return get_catalog_repository().load()


@app.get("/health")
def health() -> dict[str, object]:
    catalog = _catalog()
    return {
        "status": "ok",
        "data_source": catalog.source,
        "product_count": len(catalog.products),
        "review_count": len(catalog.reviews),
    }


@app.get("/products")
def products() -> dict[str, object]:
    return {"products": _catalog().products}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend_products(preferences: UserPreferences) -> RecommendationResponse:
    catalog = _catalog()
    return RecommendationResponse(
        recommendations=recommend(
            list(catalog.products),
            preferences,
            EvidenceIndex.from_reviews(list(catalog.reviews)),
            limit=3,
        )
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
    catalog = _catalog()
    recommendations = recommend(
        list(catalog.products),
        request.preferences,
        EvidenceIndex.from_reviews(list(catalog.reviews)),
        limit=request.limit,
    )
    return RecommendationsResponse(
        summary=_build_summary(recommendations),
        recommendations=recommendations,
        generation_mode="api-hybrid-ranking",
        metadata=RecommendationMetadata(
            data_source=catalog.source,
            product_count=len(catalog.products),
            review_count=len(catalog.reviews),
            requested_limit=request.limit,
            returned_count=len(recommendations),
            top_product_id=recommendations[0].product.product_id if recommendations else None,
        ),
    )


@app.post("/report", response_model=ReportResponse)
def report(preferences: UserPreferences) -> ReportResponse:
    catalog = _catalog()
    recommendations = recommend(
        list(catalog.products),
        preferences,
        EvidenceIndex.from_reviews(list(catalog.reviews)),
        limit=3,
    )
    return ReportResponse(
        summary=_build_summary(recommendations),
        recommendations=recommendations,
        generation_mode="deterministic",
    )


@app.post("/compare")
def compare(product_ids: list[str]) -> dict[str, object]:
    selected = [product for product in _catalog().products if product.product_id in product_ids]
    return {"products": selected}
