# GlowFit AI Portfolio Case Study

## Problem

Beauty product shoppers often rely on dense review pages to decide whether a product fits their skin type, texture preference, fragrance sensitivity, and budget. GlowFit AI turns review evidence into an explainable recommendation report.

## Dataset

Phase 1 uses committed sample fixtures for deterministic development and is designed to scale to public Amazon Beauty-style review data. The current sample set includes product metadata, ratings, review text, and a default user preference profile.

## Modeling Progression

1. Baselines: popularity and average rating.
2. Core models: content-based scoring and collaborative filtering path.
3. Advanced model: Two-Tower Retrieval for preference-product matching.
4. Explanation layer: retrieved evidence transformed into a grounded deterministic report.

## Product Experience

The demo opens directly to a report-first workspace. A reviewer can see the user profile, top recommendation, evidence snippets, model scores, and product comparison without reading code first.

## Phase 2

- Public dataset pipeline.
- Experiment tracking.
- Real LLM/RAG report generation.
- Deployment and monitoring.
- Korean-market localized demo copy.
