# GlowFit AI Portfolio Case Study

## Problem

Beauty product shoppers often rely on dense review pages to decide whether a product fits their skin type, texture preference, fragrance sensitivity, and budget. GlowFit AI turns review evidence into an explainable recommendation report.

## Dataset

Phase 1 uses committed sample fixtures for deterministic development and is designed to scale to public Amazon Beauty-style review data. The current sample set includes product metadata, ratings, review text, and a default user preference profile.

Phase 2 starts that scale-up path with Amazon Beauty-style record adapters, a JSONL ingestion pipeline, Hugging Face Dataset Viewer preview fetches, ASIN-joined public mini datasets, and offline recommender metrics. The project can now parse external metadata/review records into the local `Product` and `Review` schemas, write processed artifacts, align public reviews to product metadata, then evaluate ranked recommendations with precision@k, recall@k, and NDCG@k.

## Modeling Progression

1. Baselines: popularity and average rating.
2. Core models: content-based scoring and collaborative filtering path.
3. Advanced model: Two-Tower Retrieval for preference-product matching.
4. Explanation layer: retrieved evidence transformed into a grounded deterministic report.

## Evaluation Snapshot

The sample ranking evaluation uses a dry, fragrance-sensitive profile and marks `p_glow_gel` and `p_calm_ampoule` as relevant products.

| Metric | Value |
| --- | ---: |
| precision@1 | 1.0000 |
| recall@1 | 0.5000 |
| ndcg@1 | 1.0000 |
| precision@3 | 0.6667 |
| recall@3 | 1.0000 |
| ndcg@3 | 0.9197 |

Public artifact evaluation now uses the same metrics after processed data is generated. Products with at least one review above the relevance threshold are treated as relevant, and the report compares popularity, rating, collaborative, content, Two-Tower, and hybrid rankers.

## Product Experience

The demo opens directly to a report-first workspace. A reviewer can see the user profile, top recommendation, evidence snippets, model scores, and product comparison without reading code first.

## Phase 2

- Public dataset pipeline with joined evaluation-ready artifacts.
- Experiment tracking.
- Real LLM/RAG report generation.
- Deployment and monitoring.
- Korean-market localized demo copy.
