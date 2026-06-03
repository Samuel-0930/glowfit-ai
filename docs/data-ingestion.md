# GlowFit AI Data Ingestion

## Goal

GlowFit AI keeps small deterministic fixtures in Git, while larger public datasets should live under ignored `data/` paths. The ingestion pipeline converts Amazon Beauty-style JSONL records into the same `Product` and `Review` schemas used by the API, tests, and recommender stack.

## Input Format

The current adapter expects:

- metadata JSONL with fields such as `asin`, `title`, `brand`, `price`, `average_rating`, `rating_number`, `features`, and `categories`
- review JSONL with fields such as `reviewerID`, `asin`, `overall`, `reviewText`, and `unixReviewTime`

The parser is intentionally tolerant of missing optional fields and keeps only beauty/skincare-like metadata records.

## Local Sample Run

```bash
python scripts/ingest_amazon_beauty_jsonl.py \
  --metadata sample_data/raw_amazon_metadata.jsonl \
  --reviews sample_data/raw_amazon_reviews.jsonl \
  --output-dir data/processed/amazon_beauty_sample
```

Expected output:

```json
{
  "products_written": 2,
  "reviews_written": 2,
  "products_path": "data/processed/amazon_beauty_sample/products.json",
  "reviews_path": "data/processed/amazon_beauty_sample/reviews.json"
}
```

## Public Dataset Workflow

1. Download public metadata/review JSONL files into `data/raw/`.
2. Run the ingestion script with the raw paths.
3. Inspect `data/processed/<dataset>/products.json` and `reviews.json`.
4. Point future training or evaluation scripts at the processed directory.

Raw and processed public data are intentionally ignored by Git.

For a lightweight public-data smoke test without downloading large files, use `scripts/fetch_huggingface_preview.py`.
