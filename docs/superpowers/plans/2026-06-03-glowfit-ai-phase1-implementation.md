# GlowFit AI Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 GlowFit AI portfolio MVP: a Next.js report-first beauty recommendation app backed by a FastAPI ML service, reproducible sample pipeline, baseline/core/advanced recommendation models, review evidence retrieval, and portfolio documentation.

**Architecture:** Use a lightweight monorepo with Python ML/API code under `api/` and `src/glowfit/`, a Next.js frontend under `frontend/`, and committed `sample_data/` fixtures for deterministic tests and demos. The first working version uses local sample artifacts, then the same interfaces can be pointed at public Amazon Beauty data during model expansion.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, pytest, pandas, scikit-learn, NumPy, PyTorch, Next.js, TypeScript, React Testing Library, Playwright-ready UI structure, lucide-react.

---

## Scope Check

The approved design includes data pipeline, NLP, recommendation models, API, frontend, and portfolio documentation. This plan keeps those subsystems integrated through one Phase 1 vertical slice: first create shared contracts and deterministic sample artifacts, then make the API work, then build the frontend against the API, then add model depth and documentation. Production monitoring, scheduled retraining, and large-scale training remain outside this Phase 1 plan.

## File Structure

Create this structure:

```text
.
├── README.md
├── DESIGN.md
├── package.json
├── pyproject.toml
├── sample_data/
│   ├── products.json
│   ├── reviews.json
│   └── preferences.json
├── src/
│   └── glowfit/
│       ├── __init__.py
│       ├── artifacts.py
│       ├── data.py
│       ├── evidence.py
│       ├── models.py
│       ├── nlp.py
│       ├── ranking.py
│       └── schemas.py
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── tests/
│       └── test_api.py
├── tests/
│   ├── test_data.py
│   ├── test_evidence.py
│   ├── test_models.py
│   ├── test_nlp.py
│   └── test_ranking.py
├── scripts/
│   └── build_sample_artifacts.py
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── app-shell.tsx
│   │   ├── evidence-panel.tsx
│   │   ├── preference-form.tsx
│   │   ├── product-card.tsx
│   │   ├── product-comparison.tsx
│   │   └── recommendation-report.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── mock-data.ts
│   │   └── types.ts
│   ├── tests/
│   │   └── recommendation-report.test.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.mjs
│   └── vitest.config.ts
└── docs/
    ├── architecture.md
    ├── portfolio-case-study.md
    └── superpowers/
        ├── plans/
        └── specs/
```

Responsibilities:

- `src/glowfit/schemas.py`: shared Python domain models.
- `src/glowfit/data.py`: load and normalize products, reviews, and preferences.
- `src/glowfit/nlp.py`: deterministic beauty aspect and sentiment extraction.
- `src/glowfit/evidence.py`: review evidence indexing and retrieval.
- `src/glowfit/models.py`: baseline, content-based, collaborative filtering, and Two-Tower classes.
- `src/glowfit/ranking.py`: hybrid recommendation orchestration.
- `src/glowfit/artifacts.py`: artifact build/load boundaries.
- `api/main.py`: FastAPI routes only; no training logic.
- `frontend/lib/types.ts`: frontend contracts matching API payloads.
- `frontend/components/*`: focused UI units following `DESIGN.md`.

---

### Task 1: Repository Tooling And Skeleton

**Files:**
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `package.json`
- Create: `src/glowfit/__init__.py`
- Create: `api/__init__.py`
- Modify: `.gitignore`

- [ ] **Step 1: Create Python and workspace metadata**

Create `pyproject.toml`:

```toml
[project]
name = "glowfit-ai"
version = "0.1.0"
description = "Explainable beauty recommendation report system"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.115.0",
  "uvicorn[standard]>=0.30.0",
  "pydantic>=2.8.0",
  "pandas>=2.2.0",
  "numpy>=1.26.0",
  "scikit-learn>=1.5.0",
  "torch>=2.3.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.2.0",
  "httpx>=0.27.0",
  "ruff>=0.5.0",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests", "api/tests"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

- [ ] **Step 2: Create root npm workspace metadata**

Create `package.json`:

```json
{
  "name": "glowfit-ai-workspace",
  "private": true,
  "scripts": {
    "test": "pytest && npm --prefix frontend test",
    "lint": "ruff check . && npm --prefix frontend run lint",
    "api:dev": "uvicorn api.main:app --reload --port 8000",
    "frontend:dev": "npm --prefix frontend run dev"
  }
}
```

- [ ] **Step 3: Create initial README**

Create `README.md`:

```markdown
# GlowFit AI

Explainable beauty recommendation reports powered by review NLP, recommender models, and grounded evidence.

## Phase 1

- Next.js report-first demo app.
- FastAPI recommendation and report service.
- Baseline, core, and Two-Tower recommendation experiments.
- Review evidence retrieval and grounded explanation fallback.

## Design

- Product spec: `docs/superpowers/specs/2026-06-03-explainable-beauty-recommendation-design.md`
- Frontend design system: `DESIGN.md`

## Local Development

Python dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```
```

- [ ] **Step 4: Create package marker files**

Create `src/glowfit/__init__.py`:

```python
"""GlowFit AI domain, ML, and recommendation utilities."""
```

Create `api/__init__.py`:

```python
"""GlowFit AI FastAPI application package."""
```

- [ ] **Step 5: Confirm ignored generated files**

Run:

```bash
git status --short --ignored
```

Expected:

```text
?? README.md
?? api/
?? package.json
?? pyproject.toml
?? src/
```

- [ ] **Step 6: Commit**

```bash
git add README.md pyproject.toml package.json src/glowfit/__init__.py api/__init__.py .gitignore
git commit -m "chore: scaffold GlowFit workspace"
```

---

### Task 2: Sample Data And Shared Schemas

**Files:**
- Create: `sample_data/products.json`
- Create: `sample_data/reviews.json`
- Create: `sample_data/preferences.json`
- Create: `src/glowfit/schemas.py`
- Create: `tests/test_data.py`
- Create: `src/glowfit/data.py`

- [ ] **Step 1: Create deterministic sample product data**

Create `sample_data/products.json`:

```json
[
  {
    "product_id": "p_glow_gel",
    "name": "Glow Barrier Gel Cream",
    "category": "moisturizer",
    "brand": "Aster Lab",
    "price_usd": 24.0,
    "average_rating": 4.6,
    "review_count": 1180,
    "attributes": ["light texture", "fragrance free", "dry skin", "barrier care"]
  },
  {
    "product_id": "p_calm_ampoule",
    "name": "Calm Cica Ampoule",
    "category": "serum",
    "brand": "Seoul Leaf",
    "price_usd": 19.0,
    "average_rating": 4.4,
    "review_count": 860,
    "attributes": ["sensitive skin", "redness", "watery texture", "low irritation"]
  },
  {
    "product_id": "p_velvet_sunscreen",
    "name": "Velvet Air Sunscreen",
    "category": "sunscreen",
    "brand": "Namu Studio",
    "price_usd": 17.0,
    "average_rating": 4.1,
    "review_count": 640,
    "attributes": ["matte finish", "oily skin", "scented", "no white cast"]
  }
]
```

- [ ] **Step 2: Create deterministic sample reviews**

Create `sample_data/reviews.json`:

```json
[
  {
    "review_id": "r_001",
    "user_id": "u_1",
    "product_id": "p_glow_gel",
    "rating": 5,
    "text": "Light gel texture but still moisturizing. My dry skin felt calm and the fragrance free formula did not sting.",
    "timestamp": "2025-01-02"
  },
  {
    "review_id": "r_002",
    "user_id": "u_2",
    "product_id": "p_glow_gel",
    "rating": 4,
    "text": "Great barrier cream for winter. It can feel a little sticky under makeup.",
    "timestamp": "2025-01-03"
  },
  {
    "review_id": "r_003",
    "user_id": "u_3",
    "product_id": "p_calm_ampoule",
    "rating": 5,
    "text": "The watery texture absorbs fast and helped with redness. Very gentle for sensitive skin.",
    "timestamp": "2025-01-04"
  },
  {
    "review_id": "r_004",
    "user_id": "u_4",
    "product_id": "p_calm_ampoule",
    "rating": 3,
    "text": "Gentle but not hydrating enough for dry patches. I needed another moisturizer.",
    "timestamp": "2025-01-05"
  },
  {
    "review_id": "r_005",
    "user_id": "u_5",
    "product_id": "p_velvet_sunscreen",
    "rating": 4,
    "text": "Matte finish is excellent for oily skin and there is no white cast, but the scent is noticeable.",
    "timestamp": "2025-01-06"
  }
]
```

- [ ] **Step 3: Create deterministic sample preference data**

Create `sample_data/preferences.json`:

```json
{
  "skin_type": "dry",
  "concerns": ["redness", "barrier care"],
  "texture": "light",
  "fragrance_sensitivity": "high",
  "budget_max_usd": 25,
  "avoid": ["strong scent", "sticky finish"]
}
```

- [ ] **Step 4: Write failing tests for loaders**

Create `tests/test_data.py`:

```python
from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews


SAMPLE_DIR = Path("sample_data")


def test_load_products_maps_product_records():
    products = load_products(SAMPLE_DIR / "products.json")

    assert len(products) == 3
    assert products[0].product_id == "p_glow_gel"
    assert "fragrance free" in products[0].attributes


def test_load_reviews_maps_review_records():
    reviews = load_reviews(SAMPLE_DIR / "reviews.json")

    assert len(reviews) == 5
    assert reviews[0].rating == 5
    assert reviews[0].product_id == "p_glow_gel"


def test_load_preferences_maps_user_intake():
    preferences = load_preferences(SAMPLE_DIR / "preferences.json")

    assert preferences.skin_type == "dry"
    assert preferences.fragrance_sensitivity == "high"
    assert "barrier care" in preferences.concerns
```

- [ ] **Step 5: Run tests to verify failure**

Run:

```bash
pytest tests/test_data.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.data'
```

- [ ] **Step 6: Implement shared schemas**

Create `src/glowfit/schemas.py`:

```python
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
```

- [ ] **Step 7: Implement loaders**

Create `src/glowfit/data.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from src.glowfit.schemas import Product, Review, UserPreferences


ModelT = TypeVar("ModelT", bound=BaseModel)


def _read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_list(path: Path, model: type[ModelT]) -> list[ModelT]:
    payload = _read_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"Expected list payload in {path}")
    return [model.model_validate(item) for item in payload]


def load_products(path: Path) -> list[Product]:
    return _load_list(path, Product)


def load_reviews(path: Path) -> list[Review]:
    return _load_list(path, Review)


def load_preferences(path: Path) -> UserPreferences:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected object payload in {path}")
    return UserPreferences.model_validate(payload)
```

- [ ] **Step 8: Run tests to verify pass**

Run:

```bash
pytest tests/test_data.py -v
```

Expected:

```text
3 passed
```

- [ ] **Step 9: Commit**

```bash
git add sample_data src/glowfit/schemas.py src/glowfit/data.py tests/test_data.py
git commit -m "feat: add sample data and domain schemas"
```

---

### Task 3: Review NLP And Evidence Retrieval

**Files:**
- Create: `src/glowfit/nlp.py`
- Create: `src/glowfit/evidence.py`
- Create: `tests/test_nlp.py`
- Create: `tests/test_evidence.py`

- [ ] **Step 1: Write failing review NLP tests**

Create `tests/test_nlp.py`:

```python
from src.glowfit.nlp import extract_aspects, label_sentiment, summarize_product_reviews
from src.glowfit.schemas import Review


def test_extract_aspects_detects_beauty_keywords():
    text = "Light gel texture, fragrance free, and calming for dry skin."

    assert extract_aspects(text) == ["texture", "fragrance", "dry skin", "calming"]


def test_label_sentiment_uses_rating_and_text_cues():
    assert label_sentiment(5, "excellent and gentle") == "positive"
    assert label_sentiment(2, "sticky and irritating") == "negative"
    assert label_sentiment(3, "fine but not special") == "mixed"


def test_summarize_product_reviews_aggregates_aspects():
    reviews = [
        Review(review_id="r1", user_id="u1", product_id="p1", rating=5, text="Light and gentle texture.", timestamp="2025-01-01"),
        Review(review_id="r2", user_id="u2", product_id="p1", rating=4, text="Fragrance free and calming.", timestamp="2025-01-02"),
    ]

    summary = summarize_product_reviews(reviews)

    assert summary["product_id"] == "p1"
    assert summary["average_rating"] == 4.5
    assert "texture" in summary["top_aspects"]
    assert "fragrance" in summary["top_aspects"]
```

- [ ] **Step 2: Run NLP tests to verify failure**

Run:

```bash
pytest tests/test_nlp.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.nlp'
```

- [ ] **Step 3: Implement review NLP helpers**

Create `src/glowfit/nlp.py`:

```python
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
```

- [ ] **Step 4: Run NLP tests to verify pass**

Run:

```bash
pytest tests/test_nlp.py -v
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Write failing evidence retrieval tests**

Create `tests/test_evidence.py`:

```python
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.schemas import Review


def test_evidence_index_returns_relevant_review_snippets():
    reviews = [
        Review(review_id="r1", user_id="u1", product_id="p1", rating=5, text="Fragrance free and gentle for dry skin.", timestamp="2025-01-01"),
        Review(review_id="r2", user_id="u2", product_id="p2", rating=4, text="Matte sunscreen for oily skin.", timestamp="2025-01-02"),
    ]

    index = EvidenceIndex.from_reviews(reviews)
    snippets = index.search(product_id="p1", query_terms=["fragrance", "dry skin"], limit=2)

    assert len(snippets) == 1
    assert snippets[0].review_id == "r1"
    assert snippets[0].sentiment == "positive"
    assert snippets[0].relevance > 0
```

- [ ] **Step 6: Run evidence tests to verify failure**

Run:

```bash
pytest tests/test_evidence.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.evidence'
```

- [ ] **Step 7: Implement evidence index**

Create `src/glowfit/evidence.py`:

```python
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
```

- [ ] **Step 8: Run evidence tests to verify pass**

Run:

```bash
pytest tests/test_evidence.py -v
```

Expected:

```text
1 passed
```

- [ ] **Step 9: Commit**

```bash
git add src/glowfit/nlp.py src/glowfit/evidence.py tests/test_nlp.py tests/test_evidence.py
git commit -m "feat: add review NLP and evidence retrieval"
```

---

### Task 4: Recommendation Models And Hybrid Ranking

**Files:**
- Create: `src/glowfit/models.py`
- Create: `src/glowfit/ranking.py`
- Create: `tests/test_models.py`
- Create: `tests/test_ranking.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_models.py`:

```python
from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.models import (
    CollaborativeFilteringRecommender,
    ContentBasedRecommender,
    PopularityRecommender,
    RatingRecommender,
    TwoTowerRetrieval,
)


def test_popularity_recommender_orders_by_review_count():
    products = load_products(Path("sample_data/products.json"))
    ranked = PopularityRecommender().score(products)

    assert ranked[0][0] == "p_glow_gel"
    assert ranked[0][1] > ranked[-1][1]


def test_rating_recommender_orders_by_average_rating():
    products = load_products(Path("sample_data/products.json"))
    ranked = RatingRecommender().score(products)

    assert ranked[0][0] == "p_glow_gel"


def test_content_based_recommender_rewards_matching_preferences():
    products = load_products(Path("sample_data/products.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))

    ranked = ContentBasedRecommender().score(products, preferences)

    assert ranked[0][0] == "p_glow_gel"


def test_collaborative_filtering_recommender_uses_rating_history():
    products = load_products(Path("sample_data/products.json"))
    reviews = load_reviews(Path("sample_data/reviews.json"))

    ranked = CollaborativeFilteringRecommender().score(products, reviews)

    assert ranked[0][0] == "p_glow_gel"
    assert all(0 <= score <= 1 for _, score in ranked)


def test_two_tower_retrieval_returns_normalized_scores():
    products = load_products(Path("sample_data/products.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))

    ranked = TwoTowerRetrieval(embedding_dim=8).score(products, preferences)

    assert len(ranked) == 3
    assert all(0 <= score <= 1 for _, score in ranked)
```

- [ ] **Step 2: Run model tests to verify failure**

Run:

```bash
pytest tests/test_models.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.models'
```

- [ ] **Step 3: Implement recommendation models**

Create `src/glowfit/models.py`:

```python
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
    for avoid in preferences.avoid:
        tokens.update(avoid.lower().split())
        tokens.add(avoid.lower())
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
    def score(self, products: list[Product], preferences: UserPreferences) -> list[tuple[str, float]]:
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

    def score(self, products: list[Product], preferences: UserPreferences) -> list[tuple[str, float]]:
        preference_text = " ".join(
            [preferences.skin_type, preferences.texture, *preferences.concerns, *preferences.avoid]
        )
        user_vector = self._embed_text(preference_text)
        scores: dict[str, float] = {}
        for product in products:
            product_text = " ".join([product.name, product.category, *product.attributes])
            product_vector = self._embed_text(product_text)
            cosine = float(np.dot(user_vector, product_vector))
            scores[product.product_id] = cosine
        return _normalize(scores)
```

- [ ] **Step 4: Run model tests to verify pass**

Run:

```bash
pytest tests/test_models.py -v
```

Expected:

```text
5 passed
```

- [ ] **Step 5: Write failing hybrid ranking tests**

Create `tests/test_ranking.py`:

```python
from pathlib import Path

from src.glowfit.data import load_preferences, load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.ranking import recommend


def test_recommend_returns_ranked_recommendations_with_evidence():
    products = load_products(Path("sample_data/products.json"))
    reviews = load_reviews(Path("sample_data/reviews.json"))
    preferences = load_preferences(Path("sample_data/preferences.json"))
    evidence_index = EvidenceIndex.from_reviews(reviews)

    recommendations = recommend(products, preferences, evidence_index, limit=2)

    assert len(recommendations) == 2
    assert recommendations[0].product.product_id == "p_glow_gel"
    assert recommendations[0].fit_score > recommendations[1].fit_score
    assert recommendations[0].evidence
    assert "content" in recommendations[0].model_scores
    assert "collaborative" in recommendations[0].model_scores
    assert "two_tower" in recommendations[0].model_scores
```

- [ ] **Step 6: Run ranking tests to verify failure**

Run:

```bash
pytest tests/test_ranking.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.ranking'
```

- [ ] **Step 7: Implement hybrid ranking**

Create `src/glowfit/ranking.py`:

```python
from __future__ import annotations

from src.glowfit.evidence import EvidenceIndex
from src.glowfit.models import (
    CollaborativeFilteringRecommender,
    ContentBasedRecommender,
    PopularityRecommender,
    RatingRecommender,
    TwoTowerRetrieval,
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
    collaborative = _as_score_map(CollaborativeFilteringRecommender().score(products, evidence_index.reviews))
    content = _as_score_map(ContentBasedRecommender().score(products, preferences))
    two_tower = _as_score_map(TwoTowerRetrieval().score(products, preferences))
    query_terms = _reason_terms(preferences)

    recommendations: list[Recommendation] = []
    for product in products:
        snippets = evidence_index.search(product.product_id, query_terms=query_terms, limit=3)
        evidence_bonus = min(len(snippets) * 0.05, 0.15)
        score = (
            content.get(product.product_id, 0) * 0.40
            + two_tower.get(product.product_id, 0) * 0.30
            + collaborative.get(product.product_id, 0) * 0.15
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
                fit_score=round(score, 4),
                confidence=round(min(0.55 + len(snippets) * 0.1, 0.95), 2),
                reasons=reasons or product.attributes[:2],
                cautions=cautions,
                evidence=snippets,
                model_scores={
                    "popularity": popularity.get(product.product_id, 0),
                    "rating": rating.get(product.product_id, 0),
                    "collaborative": collaborative.get(product.product_id, 0),
                    "content": content.get(product.product_id, 0),
                    "two_tower": two_tower.get(product.product_id, 0),
                },
            )
        )

    recommendations.sort(key=lambda item: item.fit_score, reverse=True)
    return recommendations[:limit]
```

- [ ] **Step 8: Run ranking tests to verify pass**

Run:

```bash
pytest tests/test_ranking.py -v
```

Expected:

```text
1 passed
```

- [ ] **Step 9: Run all Python tests**

Run:

```bash
pytest -v
```

Expected:

```text
13 passed
```

- [ ] **Step 10: Commit**

```bash
git add src/glowfit/models.py src/glowfit/ranking.py tests/test_models.py tests/test_ranking.py
git commit -m "feat: add recommendation model stack"
```

---

### Task 5: Artifact Builder

**Files:**
- Create: `src/glowfit/artifacts.py`
- Create: `scripts/build_sample_artifacts.py`
- Create: `tests/test_artifacts.py`
- Modify: `.gitignore`

- [ ] **Step 1: Write failing artifact tests**

Create `tests/test_artifacts.py`:

```python
from pathlib import Path

from src.glowfit.artifacts import build_sample_artifacts, load_artifacts


def test_build_and_load_sample_artifacts(tmp_path: Path):
    artifact_dir = tmp_path / "artifacts"

    build_sample_artifacts(
        product_path=Path("sample_data/products.json"),
        review_path=Path("sample_data/reviews.json"),
        artifact_dir=artifact_dir,
    )
    artifacts = load_artifacts(artifact_dir)

    assert len(artifacts.products) == 3
    assert len(artifacts.reviews) == 5
    assert artifacts.evidence_index.search("p_glow_gel", ["dry skin"], limit=1)
```

- [ ] **Step 2: Run artifact tests to verify failure**

Run:

```bash
pytest tests/test_artifacts.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'src.glowfit.artifacts'
```

- [ ] **Step 3: Implement artifact build/load boundary**

Create `src/glowfit/artifacts.py`:

```python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from src.glowfit.data import load_products, load_reviews
from src.glowfit.evidence import EvidenceIndex
from src.glowfit.schemas import Product, Review


@dataclass(frozen=True)
class Artifacts:
    products: list[Product]
    reviews: list[Review]
    evidence_index: EvidenceIndex


def build_sample_artifacts(product_path: Path, review_path: Path, artifact_dir: Path) -> None:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    products = load_products(product_path)
    reviews = load_reviews(review_path)
    with (artifact_dir / "products.json").open("w", encoding="utf-8") as file:
        json.dump([product.model_dump() for product in products], file, indent=2)
    with (artifact_dir / "reviews.json").open("w", encoding="utf-8") as file:
        json.dump([review.model_dump() for review in reviews], file, indent=2)


def load_artifacts(artifact_dir: Path) -> Artifacts:
    products = load_products(artifact_dir / "products.json")
    reviews = load_reviews(artifact_dir / "reviews.json")
    return Artifacts(
        products=products,
        reviews=reviews,
        evidence_index=EvidenceIndex.from_reviews(reviews),
    )
```

- [ ] **Step 4: Create artifact build script**

Create `scripts/build_sample_artifacts.py`:

```python
from pathlib import Path

from src.glowfit.artifacts import build_sample_artifacts


if __name__ == "__main__":
    build_sample_artifacts(
        product_path=Path("sample_data/products.json"),
        review_path=Path("sample_data/reviews.json"),
        artifact_dir=Path("artifacts/sample"),
    )
    print("Built sample artifacts in artifacts/sample")
```

- [ ] **Step 5: Run artifact tests to verify pass**

Run:

```bash
pytest tests/test_artifacts.py -v
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Build local sample artifacts**

Run:

```bash
python scripts/build_sample_artifacts.py
```

Expected:

```text
Built sample artifacts in artifacts/sample
```

- [ ] **Step 7: Confirm generated artifacts are ignored**

Run:

```bash
git status --short --ignored artifacts/sample
```

Expected:

```text
!! artifacts/
```

- [ ] **Step 8: Commit**

```bash
git add src/glowfit/artifacts.py scripts/build_sample_artifacts.py tests/test_artifacts.py .gitignore
git commit -m "feat: add sample artifact builder"
```

---

### Task 6: FastAPI Recommendation Service

**Files:**
- Create: `api/main.py`
- Create: `api/tests/test_api.py`

- [ ] **Step 1: Write failing API tests**

Create `api/tests/test_api.py`:

```python
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint_returns_loaded_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["product_count"] == 3


def test_recommend_endpoint_returns_top_products():
    payload = {
        "skin_type": "dry",
        "concerns": ["redness", "barrier care"],
        "texture": "light",
        "fragrance_sensitivity": "high",
        "budget_max_usd": 25,
        "avoid": ["strong scent", "sticky finish"]
    }

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["recommendations"][0]["product"]["product_id"] == "p_glow_gel"
    assert body["recommendations"][0]["evidence"]


def test_report_endpoint_returns_grounded_sections():
    payload = {
        "skin_type": "dry",
        "concerns": ["redness", "barrier care"],
        "texture": "light",
        "fragrance_sensitivity": "high",
        "budget_max_usd": 25,
        "avoid": ["strong scent", "sticky finish"]
    }

    response = client.post("/report", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "summary" in body
    assert "recommendations" in body
    assert body["generation_mode"] == "deterministic"
```

- [ ] **Step 2: Run API tests to verify failure**

Run:

```bash
pytest api/tests/test_api.py -v
```

Expected:

```text
ModuleNotFoundError: No module named 'api.main'
```

- [ ] **Step 3: Implement FastAPI app**

Create `api/main.py`:

```python
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
```

- [ ] **Step 4: Run API tests to verify pass**

Run:

```bash
pytest api/tests/test_api.py -v
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Run API locally**

Run:

```bash
uvicorn api.main:app --port 8000
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Stop the server after confirming it starts.

- [ ] **Step 6: Commit**

```bash
git add api/main.py api/tests/test_api.py
git commit -m "feat: add FastAPI recommendation service"
```

---

### Task 7: Next.js Frontend Scaffold And Contracts

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/next.config.mjs`
- Create: `frontend/vitest.config.ts`
- Create: `frontend/app/layout.tsx`
- Create: `frontend/app/globals.css`
- Create: `frontend/lib/types.ts`
- Create: `frontend/lib/mock-data.ts`
- Create: `frontend/lib/api.ts`

- [ ] **Step 1: Create frontend package metadata**

Create `frontend/package.json`:

```json
{
  "name": "glowfit-ai-frontend",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3000",
    "build": "next build",
    "lint": "next lint",
    "test": "vitest run"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "lucide-react": "^0.468.0",
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.4.8",
    "@testing-library/react": "^16.0.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "jsdom": "^24.1.0",
    "typescript": "^5.5.0",
    "vitest": "^2.0.0"
  }
}
```

- [ ] **Step 2: Create TypeScript and Next config**

Create `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Create `frontend/next.config.mjs`:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true
};

export default nextConfig;
```

Create `frontend/vitest.config.ts`:

```ts
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true
  }
});
```

- [ ] **Step 3: Create frontend types matching API contracts**

Create `frontend/lib/types.ts`:

```ts
export type Product = {
  product_id: string;
  name: string;
  category: string;
  brand: string;
  price_usd: number;
  average_rating: number;
  review_count: number;
  attributes: string[];
};

export type EvidenceSnippet = {
  review_id: string;
  product_id: string;
  text: string;
  sentiment: "positive" | "mixed" | "negative";
  aspects: string[];
  relevance: number;
};

export type Recommendation = {
  product: Product;
  fit_score: number;
  confidence: number;
  reasons: string[];
  cautions: string[];
  evidence: EvidenceSnippet[];
  model_scores: Record<string, number>;
};

export type UserPreferences = {
  skin_type: string;
  concerns: string[];
  texture: string;
  fragrance_sensitivity: string;
  budget_max_usd: number;
  avoid: string[];
};

export type ReportResponse = {
  summary: string;
  recommendations: Recommendation[];
  generation_mode: string;
};
```

- [ ] **Step 4: Create mock data and API client**

Create `frontend/lib/mock-data.ts`:

```ts
import type { ReportResponse, UserPreferences } from "./types";

export const defaultPreferences: UserPreferences = {
  skin_type: "dry",
  concerns: ["redness", "barrier care"],
  texture: "light",
  fragrance_sensitivity: "high",
  budget_max_usd: 25,
  avoid: ["strong scent", "sticky finish"]
};

export const mockReport: ReportResponse = {
  summary:
    "Glow Barrier Gel Cream is the strongest match for a dry, fragrance-sensitive profile because it pairs light texture with barrier care evidence.",
  generation_mode: "mock",
  recommendations: [
    {
      product: {
        product_id: "p_glow_gel",
        name: "Glow Barrier Gel Cream",
        category: "moisturizer",
        brand: "Aster Lab",
        price_usd: 24,
        average_rating: 4.6,
        review_count: 1180,
        attributes: ["light texture", "fragrance free", "dry skin", "barrier care"]
      },
      fit_score: 0.94,
      confidence: 0.85,
      reasons: ["light texture", "fragrance free", "barrier care"],
      cautions: [],
      evidence: [
        {
          review_id: "r_001",
          product_id: "p_glow_gel",
          text:
            "Light gel texture but still moisturizing. My dry skin felt calm and the fragrance free formula did not sting.",
          sentiment: "positive",
          aspects: ["texture", "fragrance", "dry skin", "calming"],
          relevance: 2.2
        }
      ],
      model_scores: {
        popularity: 1,
        rating: 1,
        content: 1,
        two_tower: 0.86
      }
    }
  ]
};
```

Create `frontend/lib/api.ts`:

```ts
import { mockReport } from "./mock-data";
import type { ReportResponse, UserPreferences } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchReport(preferences: UserPreferences): Promise<ReportResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(preferences)
    });
    if (!response.ok) {
      return mockReport;
    }
    return (await response.json()) as ReportResponse;
  } catch {
    return mockReport;
  }
}
```

- [ ] **Step 5: Create app layout and global CSS**

Create `frontend/app/layout.tsx`:

```tsx
import "./globals.css";

export const metadata = {
  title: "GlowFit AI",
  description: "Explainable beauty recommendation reports"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

Create `frontend/app/globals.css`:

```css
:root {
  --canvas: #ffffff;
  --canvas-warm: #fbfbf5;
  --surface-soft: #f6f7f2;
  --ink: #111111;
  --ink-muted: #52525b;
  --ink-subtle: #71717a;
  --hairline: #e4e4e7;
  --brand-black: #000000;
  --brand-mint: #c1fbd4;
  --brand-pistachio: #d4f9e0;
  --beauty-rose: #f6c7d0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--canvas-warm);
  color: var(--ink);
  font-family: Inter, Helvetica, Arial, sans-serif;
}

button,
input,
select {
  font: inherit;
}
```

- [ ] **Step 6: Install frontend dependencies**

Run:

```bash
npm --prefix frontend install
```

Expected:

```text
added
```

- [ ] **Step 7: Commit**

```bash
git add frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/next.config.mjs frontend/vitest.config.ts frontend/app frontend/lib
git commit -m "feat: scaffold Next.js frontend contracts"
```

---

### Task 8: Report-First Frontend Components

**Files:**
- Create: `frontend/components/app-shell.tsx`
- Create: `frontend/components/preference-form.tsx`
- Create: `frontend/components/product-card.tsx`
- Create: `frontend/components/evidence-panel.tsx`
- Create: `frontend/components/recommendation-report.tsx`
- Create: `frontend/components/product-comparison.tsx`
- Create: `frontend/app/page.tsx`
- Create: `frontend/tests/recommendation-report.test.tsx`

- [ ] **Step 1: Write failing frontend component test**

Create `frontend/tests/recommendation-report.test.tsx`:

```tsx
import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RecommendationReport } from "../components/recommendation-report";
import { mockReport } from "../lib/mock-data";

describe("RecommendationReport", () => {
  it("renders summary, product, evidence, and model score labels", () => {
    render(<RecommendationReport report={mockReport} />);

    expect(screen.getByText(/Glow Barrier Gel Cream/)).toBeInTheDocument();
    expect(screen.getByText(/strongest match/)).toBeInTheDocument();
    expect(screen.getByText(/Review evidence/)).toBeInTheDocument();
    expect(screen.getByText(/two_tower/)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run frontend test to verify failure**

Run:

```bash
npm --prefix frontend test
```

Expected:

```text
Cannot find module '../components/recommendation-report'
```

- [ ] **Step 3: Implement product card**

Create `frontend/components/product-card.tsx`:

```tsx
import type { Recommendation } from "../lib/types";

export function ProductCard({ recommendation }: { recommendation: Recommendation }) {
  const { product } = recommendation;
  return (
    <article className="product-card">
      <div className="product-image" aria-hidden="true" />
      <div>
        <p className="eyebrow">{product.brand}</p>
        <h3>{product.name}</h3>
        <p className="muted">
          {product.category} · ${product.price_usd} · {product.average_rating.toFixed(1)} stars
        </p>
      </div>
      <div className="score">{Math.round(recommendation.fit_score * 100)}%</div>
      <div className="tag-row">
        {product.attributes.slice(0, 4).map((attribute) => (
          <span key={attribute} className="tag">
            {attribute}
          </span>
        ))}
      </div>
    </article>
  );
}
```

- [ ] **Step 4: Implement evidence panel**

Create `frontend/components/evidence-panel.tsx`:

```tsx
import type { Recommendation } from "../lib/types";

export function EvidencePanel({ recommendation }: { recommendation: Recommendation }) {
  return (
    <aside className="evidence-panel">
      <h2>Review evidence</h2>
      {recommendation.evidence.map((snippet) => (
        <figure key={snippet.review_id} className="evidence-card">
          <blockquote>{snippet.text}</blockquote>
          <figcaption>
            {snippet.sentiment} · relevance {snippet.relevance.toFixed(1)}
          </figcaption>
          <div className="tag-row">
            {snippet.aspects.map((aspect) => (
              <span key={aspect} className="tag tag-soft">
                {aspect}
              </span>
            ))}
          </div>
        </figure>
      ))}
    </aside>
  );
}
```

- [ ] **Step 5: Implement recommendation report**

Create `frontend/components/recommendation-report.tsx`:

```tsx
import { EvidencePanel } from "./evidence-panel";
import { ProductCard } from "./product-card";
import type { ReportResponse } from "../lib/types";

export function RecommendationReport({ report }: { report: ReportResponse }) {
  const top = report.recommendations[0];

  return (
    <section className="report-grid">
      <main className="report-main">
        <p className="eyebrow">Recommendation report</p>
        <h1>GlowFit AI</h1>
        <p className="summary">{report.summary}</p>

        <div className="recommendation-list">
          {report.recommendations.map((recommendation) => (
            <ProductCard key={recommendation.product.product_id} recommendation={recommendation} />
          ))}
        </div>

        <section className="model-panel">
          <h2>Model signals</h2>
          {Object.entries(top.model_scores).map(([model, score]) => (
            <div key={model} className="metric-row">
              <span>{model}</span>
              <strong>{score.toFixed(2)}</strong>
            </div>
          ))}
        </section>
      </main>

      <EvidencePanel recommendation={top} />
    </section>
  );
}
```

- [ ] **Step 6: Implement preference form**

Create `frontend/components/preference-form.tsx`:

```tsx
import type { UserPreferences } from "../lib/types";

type Props = {
  preferences: UserPreferences;
  onGenerate: () => void;
  isLoading: boolean;
};

export function PreferenceForm({ preferences, onGenerate, isLoading }: Props) {
  return (
    <aside className="preference-panel">
      <h2>Beauty profile</h2>
      <div className="field-group">
        <span>Skin type</span>
        <strong>{preferences.skin_type}</strong>
      </div>
      <div className="field-group">
        <span>Concerns</span>
        <strong>{preferences.concerns.join(", ")}</strong>
      </div>
      <div className="field-group">
        <span>Texture</span>
        <strong>{preferences.texture}</strong>
      </div>
      <div className="field-group">
        <span>Fragrance sensitivity</span>
        <strong>{preferences.fragrance_sensitivity}</strong>
      </div>
      <button className="primary-button" onClick={onGenerate} disabled={isLoading}>
        {isLoading ? "Generating report" : "Generate report"}
      </button>
    </aside>
  );
}
```

- [ ] **Step 7: Implement shell and app page**

Create `frontend/components/app-shell.tsx`:

```tsx
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <header className="top-nav">
        <strong>GlowFit AI</strong>
        <nav aria-label="Primary">
          <a href="#recommend">Recommend</a>
          <a href="#compare">Compare</a>
          <a href="#insights">Review Insights</a>
          <a href="#experiments">Experiments</a>
          <a href="#portfolio">Portfolio</a>
        </nav>
      </header>
      {children}
    </div>
  );
}
```

Create `frontend/components/product-comparison.tsx`:

```tsx
import type { Recommendation } from "../lib/types";

export function ProductComparison({ recommendations }: { recommendations: Recommendation[] }) {
  return (
    <section className="comparison-panel" id="compare">
      <h2>Product comparison</h2>
      <div className="comparison-table">
        {recommendations.map((item) => (
          <div key={item.product.product_id} className="comparison-row">
            <span>{item.product.name}</span>
            <span>{Math.round(item.fit_score * 100)}% fit</span>
            <span>{item.product.attributes.slice(0, 2).join(", ")}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
```

Create `frontend/app/page.tsx`:

```tsx
"use client";

import { useState } from "react";

import { AppShell } from "../components/app-shell";
import { PreferenceForm } from "../components/preference-form";
import { ProductComparison } from "../components/product-comparison";
import { RecommendationReport } from "../components/recommendation-report";
import { fetchReport } from "../lib/api";
import { defaultPreferences, mockReport } from "../lib/mock-data";
import type { ReportResponse } from "../lib/types";

export default function Page() {
  const [report, setReport] = useState<ReportResponse>(mockReport);
  const [isLoading, setIsLoading] = useState(false);

  async function handleGenerate() {
    setIsLoading(true);
    const nextReport = await fetchReport(defaultPreferences);
    setReport(nextReport);
    setIsLoading(false);
  }

  return (
    <AppShell>
      <div className="workspace" id="recommend">
        <PreferenceForm
          preferences={defaultPreferences}
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />
        <RecommendationReport report={report} />
      </div>
      <ProductComparison recommendations={report.recommendations} />
    </AppShell>
  );
}
```

- [ ] **Step 8: Add component CSS**

Append to `frontend/app/globals.css`:

```css
.top-nav {
  align-items: center;
  background: var(--canvas);
  border-bottom: 1px solid var(--hairline);
  display: flex;
  height: 64px;
  justify-content: space-between;
  padding: 0 24px;
}

.top-nav nav {
  display: flex;
  gap: 16px;
}

.top-nav a {
  color: var(--ink-muted);
  font-size: 14px;
  text-decoration: none;
}

.workspace {
  display: grid;
  gap: 20px;
  grid-template-columns: 300px minmax(0, 1fr);
  padding: 24px;
}

.preference-panel,
.evidence-panel,
.model-panel,
.comparison-panel,
.product-card {
  background: var(--canvas);
  border: 1px solid var(--hairline);
  border-radius: 8px;
  padding: 16px;
}

.preference-panel {
  height: fit-content;
}

.report-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: minmax(0, 1fr) 360px;
}

.report-main h1 {
  font-size: 40px;
  line-height: 1.1;
  margin: 0;
}

.summary {
  color: var(--ink-muted);
  font-size: 17px;
  line-height: 1.55;
}

.recommendation-list {
  display: grid;
  gap: 12px;
}

.product-card {
  display: grid;
  gap: 12px;
  grid-template-columns: 72px 1fr auto;
}

.product-image {
  aspect-ratio: 1;
  background: var(--brand-pistachio);
  border: 1px solid var(--hairline);
  border-radius: 8px;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  grid-column: 1 / -1;
}

.tag {
  background: var(--brand-pistachio);
  border-radius: 9999px;
  color: var(--ink);
  font-size: 12px;
  padding: 4px 8px;
}

.tag-soft {
  background: var(--surface-soft);
}

.score {
  background: var(--brand-mint);
  border-radius: 9999px;
  font-weight: 700;
  height: 40px;
  padding: 10px 12px;
}

.eyebrow {
  color: var(--ink-subtle);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.muted {
  color: var(--ink-muted);
}

.field-group,
.metric-row,
.comparison-row {
  border-top: 1px solid var(--hairline);
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
}

.primary-button {
  background: var(--brand-black);
  border: 0;
  border-radius: 9999px;
  color: white;
  cursor: pointer;
  height: 44px;
  padding: 0 18px;
  width: 100%;
}

.primary-button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.evidence-card {
  border-top: 1px solid var(--hairline);
  margin: 0;
  padding: 12px 0;
}

.evidence-card blockquote {
  margin: 0 0 8px;
}

.comparison-panel {
  margin: 0 24px 24px;
}

@media (max-width: 1023px) {
  .workspace,
  .report-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 9: Run frontend tests**

Run:

```bash
npm --prefix frontend test
```

Expected:

```text
1 passed
```

- [ ] **Step 10: Run frontend dev server**

Run:

```bash
npm --prefix frontend run dev
```

Expected:

```text
Local: http://localhost:3000
```

Open `http://localhost:3000` and confirm:

- The first screen is the report-first workspace.
- The preference panel appears on the left.
- The recommendation report appears in the center.
- The evidence panel appears on the right on desktop.
- Product comparison appears below.

- [ ] **Step 11: Commit**

```bash
git add frontend/app frontend/components frontend/lib frontend/tests
git commit -m "feat: add report-first frontend"
```

---

### Task 9: Documentation And Portfolio Story

**Files:**
- Modify: `README.md`
- Create: `docs/architecture.md`
- Create: `docs/portfolio-case-study.md`

- [ ] **Step 1: Update README with runnable project story**

Replace `README.md` with:

```markdown
# GlowFit AI

GlowFit AI is an explainable beauty recommendation report system. It recommends cosmetics from review data, shows why each product fits a user profile, and keeps review evidence visible beside the recommendation.

## What It Demonstrates

- Data science: EDA-ready review data, sentiment/aspect extraction, recommender comparisons.
- ML engineering: reproducible sample artifacts, FastAPI serving, typed contracts.
- AI product sense: a polished report-first Next.js experience grounded in review evidence.

## Architecture

```text
sample_data -> src/glowfit pipeline -> FastAPI -> Next.js report workspace
                         |
                         +-> review NLP, evidence retrieval, recommender scores
```

## Model Stack

| Tier | Model | Purpose |
| --- | --- | --- |
| Baseline | Popularity, average rating | Simple comparison points |
| Core | Content-based, collaborative filtering path | Recommender fundamentals |
| Advanced | Two-Tower Retrieval | Modern retrieval-style matching |
| Explanation | Evidence-backed deterministic report path | Grounded user-facing output |

## Run Locally

Install Python dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run Python tests:

```bash
pytest
```

Run API:

```bash
uvicorn api.main:app --reload --port 8000
```

Install and run frontend:

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

Open `http://localhost:3000`.

## Design Docs

- Product spec: `docs/superpowers/specs/2026-06-03-explainable-beauty-recommendation-design.md`
- Implementation plan: `docs/superpowers/plans/2026-06-03-glowfit-ai-phase1-implementation.md`
- Frontend design system: `DESIGN.md`
- Architecture notes: `docs/architecture.md`
- Portfolio case study draft: `docs/portfolio-case-study.md`
```

- [ ] **Step 2: Create architecture doc**

Create `docs/architecture.md`:

```markdown
# GlowFit AI Architecture

## Components

- `sample_data/`: deterministic fixtures for tests and demo fallback.
- `src/glowfit/`: domain schemas, data loading, review NLP, evidence retrieval, models, ranking, and artifacts.
- `api/`: FastAPI app exposing health, product, recommendation, report, and comparison endpoints.
- `frontend/`: Next.js report-first workspace using contracts that mirror the API.

## Data Flow

1. Product and review records load from sample or processed data.
2. Review NLP extracts aspects and sentiment.
3. Evidence index retrieves review snippets for a product and preference query.
4. Recommendation models score products.
5. Hybrid rank combines model scores and evidence availability.
6. FastAPI returns recommendations and deterministic report text.
7. Next.js renders report, product cards, evidence, model signals, and comparison rows.

## Phase 2 Extension Points

- Replace sample data with public Amazon Beauty processed artifacts.
- Add experiment tracking for model comparisons.
- Add real LLM/RAG generation behind the same `/report` response contract.
- Add deployment and monitoring around API and model artifacts.
```

- [ ] **Step 3: Create Notion-ready case study draft**

Create `docs/portfolio-case-study.md`:

```markdown
# GlowFit AI Portfolio Case Study

## Problem

Beauty product shoppers often rely on dense review pages to decide whether a product fits their skin type, texture preference, fragrance sensitivity, and budget. GlowFit AI turns review evidence into an explainable recommendation report.

## Dataset

Phase 1 uses committed sample fixtures for deterministic development and is designed to scale to public Amazon Beauty-style review data.

## Modeling Progression

1. Baselines: popularity and average rating.
2. Core models: content-based scoring and collaborative filtering path.
3. Advanced model: Two-Tower Retrieval for preference-product matching.
4. Explanation layer: retrieved evidence transformed into a grounded report.

## Product Experience

The demo opens directly to a report-first workspace. A reviewer can see the user profile, top recommendation, evidence snippets, model scores, and product comparison without reading code first.

## Phase 2

- Public dataset pipeline.
- Experiment tracking.
- Real LLM/RAG report generation.
- Deployment and monitoring.
- Korean-market localized demo copy.
```

- [ ] **Step 4: Run documentation checks**

Run:

```bash
rg -n "DECISION[_]REQUIRED|FIELD[_]INCOMPLETE" README.md docs
```

Expected:

```text
```

- [ ] **Step 5: Run full tests**

Run:

```bash
pytest -v
npm --prefix frontend test
```

Expected:

```text
Python tests pass
Frontend tests pass
```

- [ ] **Step 6: Commit**

```bash
git add README.md docs/architecture.md docs/portfolio-case-study.md
git commit -m "docs: add portfolio project story"
```

---

### Task 10: Final Verification And Demo Readiness

**Files:**
- Modify: `README.md` if commands or screenshots need correction after verification.

- [ ] **Step 1: Run full Python test suite**

Run:

```bash
pytest -v
```

Expected:

```text
All Python tests pass
```

- [ ] **Step 2: Run frontend tests**

Run:

```bash
npm --prefix frontend test
```

Expected:

```text
All frontend tests pass
```

- [ ] **Step 3: Build frontend**

Run:

```bash
npm --prefix frontend run build
```

Expected:

```text
Compiled successfully
```

- [ ] **Step 4: Start API and frontend together**

Terminal A:

```bash
uvicorn api.main:app --reload --port 8000
```

Terminal B:

```bash
npm --prefix frontend run dev
```

Expected:

```text
API available at http://localhost:8000
Frontend available at http://localhost:3000
```

- [ ] **Step 5: Browser QA**

Open `http://localhost:3000` and verify:

- Page loads without console errors.
- Generate report button keeps the app usable when the API is running.
- Generate report button falls back to mock data when the API is stopped.
- Desktop layout uses left profile, center report, right evidence.
- Mobile viewport stacks profile, report, and evidence without overlap.
- Model signals show `popularity`, `rating`, `collaborative`, `content`, and `two_tower`.

- [ ] **Step 6: Verify git state**

Run:

```bash
git status --short
```

Expected:

```text
```

- [ ] **Step 7: Create final verification commit only if files changed**

If README or docs were corrected during verification:

```bash
git add README.md docs
git commit -m "docs: finalize demo verification notes"
```

If no files changed, do not create an empty commit.

---

## Self-Review Notes

Spec coverage:

- Data loading and sample fixtures: Task 2.
- Review NLP and evidence retrieval: Task 3.
- Baseline/Core/Advanced recommendation models: Task 4.
- Artifact boundary: Task 5.
- FastAPI routes: Task 6.
- Next.js report-first frontend: Tasks 7 and 8.
- Portfolio documentation: Task 9.
- Verification: Task 10.

Type consistency:

- Python API uses `UserPreferences`, `Recommendation`, and `EvidenceSnippet` from `src/glowfit/schemas.py`.
- Frontend uses matching `UserPreferences`, `Recommendation`, and `EvidenceSnippet` in `frontend/lib/types.ts`.
- API `/report` returns the shape consumed by `frontend/lib/api.ts`.

Execution order:

- Tasks should be completed in order because later tasks depend on schemas, sample data, and API contracts from earlier tasks.
