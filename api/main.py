from __future__ import annotations

import os
from math import isfinite

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.glowfit.catalog import (
    CachedCatalogRepository,
    Catalog,
    CatalogRepository,
    CatalogUnavailableError,
    get_catalog_repository,
)
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend
from src.glowfit.schemas import ProductId, Recommendation, UserPreferences


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]


class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    limit: int = Field(default=3, ge=1, le=10)


class CompareRequest(BaseModel):
    product_ids: list[ProductId] = Field(min_length=1, max_length=20)


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


def cors_origins() -> list[str]:
    return [
        origin.strip()
        for origin in os.getenv("GLOWFIT_CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]


def is_production() -> bool:
    return os.getenv("GLOWFIT_ENV", "development").lower() == "production"


def trusted_hosts() -> list[str]:
    configured_hosts = os.getenv("GLOWFIT_TRUSTED_HOSTS", "").split(",")
    return [host.strip() for host in configured_hosts if host.strip()]


def api_docs_enabled() -> bool:
    return not is_production()


def catalog_cache_ttl_seconds() -> float:
    raw_value = os.getenv("GLOWFIT_CATALOG_CACHE_TTL_SECONDS", "60")
    try:
        ttl_seconds = float(raw_value)
    except ValueError as error:
        raise RuntimeError(
            "GLOWFIT_CATALOG_CACHE_TTL_SECONDS must be a non-negative number"
        ) from error
    if not isfinite(ttl_seconds) or ttl_seconds < 0:
        raise RuntimeError("GLOWFIT_CATALOG_CACHE_TTL_SECONDS must be a non-negative number")
    return ttl_seconds


if is_production() and not trusted_hosts():
    raise RuntimeError("GLOWFIT_TRUSTED_HOSTS must be configured in production")

catalog_cache_ttl_seconds()


app = FastAPI(
    title="GlowFit AI API",
    version="0.1.0",
    docs_url="/docs" if api_docs_enabled() else None,
    redoc_url="/redoc" if api_docs_enabled() else None,
    openapi_url="/openapi.json" if api_docs_enabled() else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)
if is_production():
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts())

_catalog_repository: CatalogRepository | None = None


def _catalog() -> Catalog:
    global _catalog_repository
    if _catalog_repository is None:
        _catalog_repository = CachedCatalogRepository(
            repository=get_catalog_repository(),
            ttl_seconds=catalog_cache_ttl_seconds(),
        )
    return _catalog_repository.load()


@app.exception_handler(CatalogUnavailableError)
async def catalog_unavailable_handler(_: Request, __: CatalogUnavailableError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": "추천 카탈로그에 일시적으로 연결할 수 없습니다. 잠시 후 다시 시도해 주세요."
        },
    )


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
def compare(request: CompareRequest) -> dict[str, object]:
    selected = [
        product for product in _catalog().products if product.product_id in request.product_ids
    ]
    return {"products": selected}
