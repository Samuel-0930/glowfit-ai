# GlowFit AI Architecture

## Components

- `sample_data/`: deterministic product, review, and preference fixtures for tests and the default JSON catalog.
- `src/glowfit/`: domain schemas, data loading, review NLP, evidence retrieval, recommendation models, hybrid ranking, and artifact utilities.
- `src/glowfit/datasets.py`: adapters for Amazon Beauty-style metadata and review records.
- `src/glowfit/ingestion.py`: JSONL ingestion pipeline for public-data artifacts.
- `src/glowfit/huggingface_joined_preview.py`: Hugging Face Dataset Viewer workflow for ASIN-matched public mini datasets.
- `src/glowfit/evaluation.py`: ranking metrics for offline recommender comparison.
- `src/glowfit/public_evaluation.py`: processed public artifact evaluation across baseline, core, advanced, and hybrid rankers.
- `src/glowfit/catalog.py`: JSON and Supabase catalog repositories plus an in-process TTL cache for
  remote reads. The Supabase repository uses a server-only Secret key or legacy service-role key.
- `api/`: FastAPI app exposing health, product, recommendation, report, and comparison endpoints.
  Catalog connectivity failures are returned as HTTP `503` responses.
- `frontend/`: Next.js workspace that calls FastAPI for recommendations and presents an explicit
  error state instead of substituting client-side mock recommendations when the API fails.

## Data Flow

1. Raw public metadata/review JSONL files are staged under ignored `data/raw/` paths.
2. Ingestion converts Amazon Beauty-style records into processed `Product` and `Review` artifacts.
3. Hugging Face preview scripts can create small public artifacts, including ASIN-joined product/review pairs.
4. The catalog repository loads product and review records from sample fixtures by default, or from
   Supabase when `GLOWFIT_CATALOG_SOURCE=supabase` is configured.
5. Review NLP extracts aspects and sentiment labels from review text.
6. Evidence index retrieves review snippets for a product and preference query.
7. Deterministic baselines score products with popularity, rating, tag-based content matching,
   review-average scoring, and hash-vector retrieval similarity.
8. Hybrid rank combines model scores and evidence availability into `Recommendation` objects.
9. Offline evaluation measures the ranked product IDs against relevant products using precision, recall, and NDCG.
10. The API caches the loaded catalog for `GLOWFIT_CATALOG_CACHE_TTL_SECONDS` (60 seconds by
    default), then returns recommendations and report text through typed endpoints.
11. Supabase connectivity failures are converted to HTTP `503`; no fallback recommendation is
    generated for a failed API request.
12. Next.js renders the user profile, API report summary, data-source label, product cards,
    evidence snippets, model signals, comparison rows, or an explicit request error.

## Phase 2 Extension Points

- Replace the small catalog with validated processed public artifacts through the dataset adapters.
- Add experiment tracking and model registry on top of the ranking metrics.
- Add real LLM/RAG generation behind the existing `/report` response contract.
- Add deployment, latency monitoring, and model/data drift checks around API and model artifacts.
- Add localized Korean-market demo copy while keeping data collection legally safe.
