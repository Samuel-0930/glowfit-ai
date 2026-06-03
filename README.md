# GlowFit AI

GlowFit AI is an explainable beauty recommendation report system. It recommends cosmetics from review data, shows why each product fits a user profile, and keeps review evidence visible beside the recommendation.

![GlowFit AI report workspace](docs/assets/glowfit-report-desktop.png)

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

## Evaluation

Phase 2 adds offline ranking evaluation so model changes can be compared instead of judged by demo output alone.

Convert Amazon Beauty-style JSONL into GlowFit processed artifacts:

```bash
python scripts/ingest_amazon_beauty_jsonl.py \
  --metadata sample_data/raw_amazon_metadata.jsonl \
  --reviews sample_data/raw_amazon_reviews.jsonl \
  --output-dir data/processed/amazon_beauty_sample
```

Generated files are written under ignored `data/processed/` paths so large public artifacts stay out of Git.

Fetch a small public Hugging Face preview:

```bash
python scripts/fetch_huggingface_preview.py --length 25
```

Fetch an ASIN-joined Hugging Face mini dataset for public-data evaluation:

```bash
python scripts/fetch_huggingface_joined_preview.py \
  --target-matches 25 \
  --max-review-rows 250
```

Evaluate processed public-data artifacts:

```bash
python scripts/evaluate_public_artifacts.py \
  --artifact-dir data/processed/hf_joined_preview \
  --output artifacts/public_evaluation.json
```

```bash
python scripts/evaluate_sample_recommenders.py
```

Current sample metrics:

| Metric | Value |
| --- | ---: |
| precision@1 | 1.0000 |
| recall@1 | 0.5000 |
| ndcg@1 | 1.0000 |
| precision@3 | 0.6667 |
| recall@3 | 1.0000 |
| ndcg@3 | 0.9197 |

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
- Data ingestion notes: `docs/data-ingestion.md`
- Hugging Face preview notes: `docs/huggingface-preview.md`
- Hugging Face joined preview notes: `docs/huggingface-joined-preview.md`
- Evaluation notes: `docs/evaluation.md`
- Portfolio case study draft: `docs/portfolio-case-study.md`
