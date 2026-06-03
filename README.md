# GlowFit AI

GlowFit AI is an explainable beauty recommendation report system. It recommends cosmetics from review data, shows why each product fits a user profile, and keeps review evidence visible beside the recommendation.

## What It Demonstrates

- Data science: review data preparation, sentiment/aspect extraction, recommender comparisons, and evaluation-ready tests.
- ML engineering: reproducible sample artifacts, FastAPI serving, typed contracts, and a clean model/API boundary.
- AI product sense: a polished report-first Next.js experience grounded in visible review evidence.

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
