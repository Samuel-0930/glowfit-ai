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
