# GlowFit AI Evaluation

## Goal

Recommendation demos can look convincing even when the ranking logic is weak. GlowFit AI adds offline ranking metrics so model changes can be compared with repeatable evidence.

## Metrics

- `precision@k`: how many of the top-k recommendations are relevant.
- `recall@k`: how many known relevant products appear in the top-k recommendations.
- `ndcg@k`: whether relevant products appear near the top of the ranking.

## Sample Run

```bash
python scripts/evaluate_sample_recommenders.py
```

Current deterministic sample output:

```json
{
  "profile": "default_dry_sensitive_profile",
  "relevant_product_ids": [
    "p_glow_gel",
    "p_calm_ampoule"
  ],
  "ranked_product_ids": [
    "p_glow_gel",
    "p_velvet_sunscreen",
    "p_calm_ampoule"
  ],
  "metrics": {
    "precision@1": 1.0,
    "recall@1": 0.5,
    "ndcg@1": 1.0,
    "precision@3": 0.6667,
    "recall@3": 1.0,
    "ndcg@3": 0.9197
  }
}
```

## Public Data Path

`src/glowfit/datasets.py` maps Amazon Beauty-style records into the local domain schema:

- metadata records -> `Product`
- review records -> `Review`

This keeps the API and frontend contracts stable while the data source grows from deterministic fixtures to public review datasets.

## Public Artifact Evaluation

After generating or ingesting a processed artifact directory with `products.json` and `reviews.json`, run:

```bash
python scripts/evaluate_public_artifacts.py \
  --artifact-dir data/processed/hf_joined_preview \
  --output artifacts/public_evaluation.json \
  --relevant-rating-threshold 4 \
  --k-values 1,3,5
```

The public artifact evaluator treats products with at least one review at or above the rating threshold as relevant. It compares these ranking outputs:

- popularity
- rating
- collaborative
- content
- two_tower
- hybrid

The output JSON includes product/review counts, the relevance rule, ranked product IDs per model, and precision@k, recall@k, and NDCG@k metrics.
