# GlowFit AI Architecture

## Components

- `sample_data/`: deterministic product, review, and preference fixtures for tests and demo fallback.
- `src/glowfit/`: domain schemas, data loading, review NLP, evidence retrieval, recommendation models, hybrid ranking, and artifact utilities.
- `src/glowfit/datasets.py`: adapters for Amazon Beauty-style metadata and review records.
- `src/glowfit/ingestion.py`: JSONL ingestion pipeline for public-data artifacts.
- `src/glowfit/huggingface_joined_preview.py`: Hugging Face Dataset Viewer workflow for ASIN-matched public mini datasets.
- `src/glowfit/evaluation.py`: ranking metrics for offline recommender comparison.
- `src/glowfit/public_evaluation.py`: processed public artifact evaluation across baseline, core, advanced, and hybrid rankers.
- `api/`: FastAPI app exposing health, product, recommendation, report, and comparison endpoints.
- `frontend/`: Next.js report-first workspace using TypeScript contracts that mirror the API responses.

## Data Flow

1. Raw public metadata/review JSONL files are staged under ignored `data/raw/` paths.
2. Ingestion converts Amazon Beauty-style records into processed `Product` and `Review` artifacts.
3. Hugging Face preview scripts can create small public artifacts, including ASIN-joined product/review pairs.
4. Product and review records load from sample fixtures or processed public data.
5. Review NLP extracts aspects and sentiment labels from review text.
6. Evidence index retrieves review snippets for a product and preference query.
7. Recommendation models score products with popularity, rating, content, collaborative, and Two-Tower signals.
8. Hybrid rank combines model scores and evidence availability into `Recommendation` objects.
9. Offline evaluation measures the ranked product IDs against relevant products using precision, recall, and NDCG.
10. FastAPI returns recommendations and deterministic report text through typed endpoints.
11. Next.js renders the user profile, report summary, product cards, evidence snippets, model signals, and comparison rows.

## Phase 2 Extension Points

- Replace sample fixtures with processed public Amazon Beauty artifacts through the dataset adapters.
- Add experiment tracking and model registry on top of the ranking metrics.
- Add real LLM/RAG generation behind the existing `/report` response contract.
- Add deployment, latency monitoring, and model/data drift checks around API and model artifacts.
- Add localized Korean-market demo copy while keeping data collection legally safe.
