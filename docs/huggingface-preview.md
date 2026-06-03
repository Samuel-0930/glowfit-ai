# GlowFit AI Hugging Face Preview

## Goal

This step proves that GlowFit AI can pull real public rows from Hugging Face Dataset Viewer and map them into the same processed artifacts used by the local recommender stack.

## Verified Datasets

The current preview script uses public, Dataset Viewer-enabled mirrors:

- Product metadata: `smartcat/Amazon_All_Beauty_2023`
- Reviews: `jhan21/amazon-beauty-reviews-dataset`

The original `McAuley-Lab/Amazon-Reviews-2023` dataset is useful as a source reference, but its Dataset Viewer preview is not enabled, so the project uses Viewer-enabled public mirrors for lightweight preview automation.

## Run Preview Fetch

```bash
python scripts/fetch_huggingface_preview.py \
  --length 25 \
  --output-dir data/processed/hf_preview
```

Expected shape:

```json
{
  "products_written": 25,
  "reviews_written": 25,
  "products_path": "data/processed/hf_preview/products.json",
  "reviews_path": "data/processed/hf_preview/reviews.json"
}
```

## Current Limitation

The metadata and review previews come from separate public mirrors, so the first N metadata rows and first N review rows are not guaranteed to share the same ASINs. This preview step validates schema mapping and public-data access.

Use `scripts/fetch_huggingface_joined_preview.py` when the next step needs products and reviews aligned by ASIN for ranking evaluation or evidence retrieval experiments.
