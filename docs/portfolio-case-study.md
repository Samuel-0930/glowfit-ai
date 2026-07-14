# GlowFit AI Portfolio Case Study

## Portfolio Snapshot

- Live demo: https://glowfit-web.vercel.app
- Demo video: [docs/assets/glowfit-demo.webm](assets/glowfit-demo.webm)
- Repository guide: [README](../README.md)
- Stack: Next.js, FastAPI, Supabase, Vercel, GitHub Actions
- Production catalog: 100 face-skincare products, 1,074 reviews

### Resume-ready description

> Next.js·FastAPI·Supabase·Vercel로 구현한 설명 가능한 스킨케어 추천 시스템. 피부 프로필을 반영해 상위 3개를 동적으로 랭킹하고, 점수만 제시하지 않고 제품 태그·리뷰 snippet·주의 신호로 추천 근거를 함께 제공했다. 100개 제품과 1,074개 리뷰를 운영 카탈로그로 적재하고 GitHub Actions의 배포 후 smoke check를 구성했다.

이 프로젝트의 핵심은 “추천 결과”가 아니라 **입력 → 랭킹 → 근거 검증**이 연결된 사용자 경험을 만들었다는 점이다. 데모에서는 빠른 체험 프로필을 선택해 실제 운영 API가 반환하는 후보, 비교 기준, 리뷰 근거를 차례로 확인할 수 있다.

## Problem

Beauty product shoppers often rely on dense review pages to decide whether a product fits their skin type, texture preference, fragrance sensitivity, and budget. GlowFit AI turns review evidence into an explainable recommendation report.

## Dataset

Phase 1 uses committed sample fixtures for deterministic development and is designed to scale to public Amazon Beauty-style review data. The current sample set includes product metadata, ratings, review text, and a default user preference profile.

Phase 2 starts that scale-up path with Amazon Beauty-style record adapters, a JSONL ingestion pipeline, Hugging Face Dataset Viewer preview fetches, ASIN-joined public mini datasets, and offline recommender metrics. The project can now parse external metadata/review records into the local `Product` and `Review` schemas, write processed artifacts, align public reviews to product metadata, then evaluate ranked recommendations with precision@k, recall@k, and NDCG@k.

## Modeling Progression

1. Baselines: popularity and average rating.
2. Core baselines: tag-based content scoring and product-level observed-review average scoring.
3. Retrieval-inspired baseline: hash-vector cosine similarity for preference-product matching;
   it is not a trained Two-Tower model.
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

Public artifact evaluation now uses the same metrics after processed data is generated. Products with at least one review above the relevance threshold are treated as relevant, and the report compares popularity, rating, review-average, content, hash-vector similarity, and hybrid rankers.

The committed three-product artifact is deliberately an exploratory fixture, not a benchmark. Its current
relevance rule labels all three products relevant, so the UI and JSON report mark the run as
`comparative_ready: false` rather than treating 1.0 scores as proof of model quality. This is a product
decision: the evaluation page shows the limitation next to the result, while the pipeline remains
reproducible for a larger ASIN-joined catalog.

## Product Experience

The demo opens to a profile-first workspace. After entering skin conditions, a reviewer can inspect
the API-backed top recommendation, evidence snippets, model scores, and product comparison without
reading code first.

## Production Evidence

- Live application: https://glowfit-web.vercel.app
- API health endpoint: https://glowfit-api.vercel.app/health
- The Next.js client calls a separately deployed FastAPI API through an environment-configured base URL.
- The API uses a TTL catalog cache with stale-data fallback, explicit CORS origins, trusted-host validation,
  and a Vercel Firewall rate-limit rule for `/recommendations`.

## Interview Narrative

The most important engineering choice was to avoid a static recommendation mock. I designed a profile-to-
ranking-to-evidence flow, then made its failure modes visible: unavailable catalog data returns an API error,
small evaluation data is labeled exploratory, and the deployed client is constrained to the production API
origin. The project does not claim a trained Two-Tower model or production-quality ranking lift; it shows a
clear baseline, an explainable API contract, a repeatable evaluation path, and the next experiment needed to
validate the ranking on a larger, non-degenerate joined catalog.

## Phase 2

- Public dataset pipeline with joined evaluation-ready artifacts.
- Experiment tracking.
- Real LLM/RAG report generation.
- Production deployment, CORS validation, and request protection.
- Korean-market localized demo copy.
