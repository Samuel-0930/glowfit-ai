# GlowFit AI Hugging Face Joined Preview

## Goal

The basic Hugging Face preview proves public-data access and schema mapping. This joined preview goes one step further: it reads public review rows, searches metadata by ASIN, and writes only products with matching reviews.

That makes the output useful for ranking evaluation, evidence retrieval checks, and future model experiments.

## Run Joined Fetch

```bash
python scripts/fetch_huggingface_joined_preview.py \
  --target-matches 25 \
  --max-review-rows 250 \
  --output-dir data/processed/hf_joined_preview
```

The CLI prints progress to stderr while it pages review rows and searches metadata ASINs. If Hugging Face Dataset Viewer search is slow, lower the per-ASIN timeout:

```bash
python scripts/fetch_huggingface_joined_preview.py \
  --target-matches 25 \
  --max-review-rows 250 \
  --metadata-search-timeout 3
```

Expected shape:

```json
{
  "target_matches": 25,
  "review_rows_scanned": 250,
  "metadata_searches": 120,
  "products_written": 25,
  "reviews_written": 25,
  "products_path": "data/processed/hf_joined_preview/products.json",
  "reviews_path": "data/processed/hf_joined_preview/reviews.json",
  "summary_path": "data/processed/hf_joined_preview/summary.json"
}
```

The exact scan/search counts depend on Dataset Viewer index availability and the public mirror contents.

## Evaluate Joined Artifacts

Once the joined artifact directory contains matched products and reviews, evaluate the model rankings:

```bash
python scripts/evaluate_public_artifacts.py \
  --artifact-dir data/processed/hf_joined_preview \
  --output artifacts/public_evaluation.json
```

## Method

1. Page review rows from `jhan21/amazon-beauty-reviews-dataset`.
2. Extract each review ASIN.
3. Query `smartcat/Amazon_All_Beauty_2023` through the Dataset Viewer `/search` endpoint.
4. Keep only exact ASIN metadata matches.
5. Write `products.json`, `reviews.json`, and `summary.json` under ignored `data/processed/`.

## Portfolio Value

This step turns the project from a demo fixture into a reproducible public-data workflow. It shows practical data engineering choices: tolerant parsing, key-based joins, deterministic artifacts, smoke-testable scripts, and clear separation between committed fixtures and ignored public-data outputs.

## Operational Note

Hugging Face Dataset Viewer search can return a temporary "dataset index is loading" response or hang until timeout while a public mirror is being indexed. The local unit tests use fake fetch/search functions so join behavior remains deterministic; live fetches should be treated as smoke tests.
