# Explainable Beauty Recommendation Report System - Design

## Summary

Build a portfolio-grade data science and ML engineering project: an explainable beauty commerce recommendation report system. The product recommends cosmetics from public review data, explains why each product fits a user's preferences, shows review evidence, compares products, and exposes model/analysis details for reviewers.

Phase 1 targets a polished, interview-ready product using public Amazon Beauty-style data, Next.js, FastAPI, reproducible ML notebooks/scripts, baseline/core/advanced recommender experiments, review NLP, and an LLM/RAG explanation layer. Phase 2 extends the same system toward MLOps: scheduled pipelines, monitoring, retraining, and deployment hardening.

## Portfolio Goal

The project should make the candidate look balanced across three dimensions:

- Data science: EDA, review NLP, recommender modeling, evaluation, and experiment interpretation.
- ML engineering: reproducible pipeline, model artifacts, API serving, clear architecture, and deployable app structure.
- AI product sense: a polished report-first user experience that makes model outputs understandable and useful.

The final portfolio package should include:

- GitHub repository with code, README, architecture diagram, model comparison table, API docs, and reproducible run instructions.
- Notion case study with problem framing, dataset decisions, modeling trade-offs, evaluation, failures, lessons learned, and Phase 2 roadmap.
- Demo app using a report-first layout, guided by the root `DESIGN.md`.

## Product Concept

Project name for Phase 1: **GlowFit AI**

User-facing concept:

> A beauty shopping assistant that recommends products based on skin type, concerns, texture preferences, fragrance sensitivity, and budget, then explains each recommendation using review evidence.

Reviewer-facing concept:

> A portfolio system that demonstrates how review text, product metadata, recommender models, and RAG-style explanation can be combined into a usable AI commerce product.

## Target Users

Primary demo user:

- A consumer looking for cosmetics that match personal preferences and constraints.

Secondary portfolio user:

- An interviewer reviewing the candidate's data science, ML engineering, and AI product skills.

## Phase 1 Scope

### In Scope

- Public review/product data ingestion.
- EDA and dataset filtering.
- Review text preprocessing.
- Review NLP features: sentiment, aspects, pro/con candidates, and attribute tags.
- Recommendation models:
  - Baseline: popularity, average rating, simple content similarity.
  - Core: content-based recommendation and collaborative filtering.
  - Advanced: Two-Tower Retrieval.
- Review evidence retrieval for recommended products.
- LLM/RAG recommendation report generation using retrieved evidence.
- FastAPI service for recommendations, reports, product search, comparison, and health checks.
- Next.js report-first demo app.
- Portfolio tab inside the app.
- GitHub README and Notion case-study structure.

### Out Of Scope For Phase 1

- Production-grade monitoring.
- Scheduled retraining.
- Real user authentication.
- Payments, cart, checkout, or inventory systems.
- Scraping restricted commercial sites.
- Full Korean production dataset collection.
- Large-scale distributed training.

## Phase 2 Expansion

Phase 2 should build on a completed Phase 1 rather than replace it.

Planned additions:

- Automated data pipeline with scheduled batch processing.
- Model registry and experiment tracking.
- Batch recommendation generation.
- Model/data drift monitoring.
- API latency and error monitoring.
- Deployment hardening.
- More advanced recommender comparison, such as LightGCN or cross-encoder reranking.
- Korean-market demo adaptation using synthetic localized demo copy while the model remains trained/evaluated on public review data.

## Data Strategy

Primary data source:

- Public Amazon Beauty-style review and product metadata datasets.

Data fields expected:

- User id.
- Product id.
- Rating.
- Review text.
- Review timestamp.
- Product title.
- Product category.
- Product metadata when available.

Filtering strategy:

- Keep a manageable subset suitable for local training and demo responsiveness.
- Remove products and users with too few interactions for collaborative filtering.
- Keep enough review text per product to support evidence retrieval.
- Preserve a held-out evaluation split.

Data artifacts:

- Raw data should live under `data/raw/` and stay out of git.
- Processed data should live under `data/processed/` and stay out of git.
- Small sample/demo fixtures should be committed under `sample_data/` when needed for tests or UI demos.

## ML And NLP Design

### Review NLP

The review NLP layer converts raw reviews into interpretable signals:

- Sentiment score or label.
- Aspect tags such as texture, scent, irritation, moisture, coverage, durability, packaging, price, and repurchase intent.
- Positive and negative evidence snippets.
- Product-level aggregated attributes.
- Embeddings for semantic retrieval.

Implementation can combine:

- Rule-based keyword extraction for beauty-specific tags.
- Sentence embedding models for semantic grouping.
- Lightweight sentiment classifier or pretrained sentiment model.
- LLM-assisted labeling is allowed only for a small validation/sample set and must be documented when used.

### Recommendation Models

The model stack should show progression from simple to advanced.

#### Baseline

- Popularity recommender.
- Average rating recommender.
- Simple content similarity based on product metadata and aggregated review text.

Purpose:

- Establish comparison points.
- Make improvements easy to explain in README and Notion.

#### Core Models

- Content-based recommender:
  - Product profile from metadata, review embeddings, and extracted attributes.
  - User preference vector from intake form.
  - Similarity scoring between preference vector and product profiles.

- Collaborative filtering:
  - User-product rating/interactions matrix.
  - Matrix factorization for explicit ratings, with implicit-feedback conversion used only if the chosen dataset subset lacks reliable explicit-rating labels.

Purpose:

- Demonstrate recommender-system fundamentals.
- Compare text/metadata-based personalization against interaction-based recommendation.

#### Advanced Model

- Two-Tower Retrieval:
  - User/preference tower encodes user profile or interaction history.
  - Product tower encodes product metadata, review summary, and attribute signals.
  - Dot-product or cosine similarity retrieves candidate products.

Purpose:

- Show a modern recommendation architecture that maps cleanly to user preference intake and product representation.
- Keep Phase 1 advanced enough without expanding into too many model families.

### Ranking Strategy

Phase 1 should compare models and choose a final serving strategy based on:

- Offline recommendation metrics.
- Quality of explanations.
- Demo reliability.
- Latency and implementation complexity.

The final app should use a hybrid rank:

- Candidate generation from content-based and/or Two-Tower Retrieval.
- Collaborative filtering score when user interaction history is available.
- Evidence availability bonus.
- Penalty for detected mismatch with user avoid preferences.

## LLM/RAG Explanation Design

The LLM must not invent unsupported claims. It should generate a polished report only from:

- User preference intake.
- Recommended product metadata.
- Model scores.
- Retrieved review snippets.
- Extracted sentiment/aspect tags.

Report sections:

- Short recommendation summary.
- Why this product fits.
- Review evidence.
- Pros.
- Cons or cautions.
- Best-for user segment.
- Avoid-if user segment.

Fallback behavior:

- If LLM/RAG fails, the API should still return model-based recommendations and structured evidence.
- The UI should clearly mark generated explanation as unavailable instead of hiding the recommendation result.

## API Design

FastAPI should expose a small, focused API:

- `GET /health`
  - Returns service status and loaded artifact summary.

- `GET /products`
  - Searches or lists products.

- `POST /recommend`
  - Accepts user preferences and returns ranked recommendations with model scores and evidence ids.

- `POST /report`
  - Accepts user preferences and recommendation candidates, returns generated report text plus structured evidence.

- `POST /compare`
  - Accepts product ids and returns comparison fields, NLP summaries, and model signals.

API responses should be typed with Pydantic models. The service should be usable independently from the frontend.

## Frontend Design

Frontend stack:

- Next.js.
- TypeScript.
- Component-driven UI.
- Styling guided by the root `DESIGN.md`.

Primary layout:

- Report-first workspace.
- Persistent top navigation.
- Tabs: Recommend, Compare, Review Insights, Experiments, Portfolio.

Main user flow:

1. User enters skin type, concerns, texture preference, fragrance sensitivity, avoid preferences, and budget.
2. App calls recommendation API.
3. App displays Top 3 recommended products.
4. User opens recommendation report.
5. Evidence panel shows review snippets, aspect tags, sentiment, and model signals.
6. User compares products or opens analysis/portfolio tabs.

Required UI states:

- Empty state.
- Loading state.
- Generated recommendation state.
- Product comparison state.
- API error state.
- LLM/RAG unavailable state.

## Portfolio Documentation

### GitHub README

README should include:

- Project one-liner.
- Demo screenshot or GIF.
- Problem definition.
- Architecture diagram.
- Dataset source and limitations.
- Model stack summary.
- Evaluation summary.
- How to run locally.
- API endpoint summary.
- Frontend design note pointing to `DESIGN.md`.
- Notion case study link.
- Phase 2 roadmap.

### Notion Case Study

Notion should be written like a product/data case study:

- Why this problem.
- Why beauty reviews.
- Dataset constraints.
- EDA findings.
- Modeling decisions.
- Baseline/Core/Advanced comparison.
- How explanation grounding works.
- What failed or was simplified.
- What Phase 2 would add.
- What the candidate learned.

The Notion page should be readable by non-engineers but include enough technical depth for data/ML interviewers.

## Evaluation Plan

Recommendation evaluation:

- Precision@K or Recall@K where interaction splits allow.
- NDCG@K or MAP@K if ranking labels are available.
- Coverage.
- Diversity.
- Popularity bias check.

Review NLP evaluation:

- Manual spot-check of aspect extraction.
- Sentiment sanity checks.
- Evidence relevance review.

Explanation evaluation:

- Groundedness: explanation claims map to retrieved evidence.
- Usefulness: report helps a user understand why a product fits.
- Caution quality: avoid-if section reflects negative/mismatch signals.

Engineering evaluation:

- API returns typed responses.
- Frontend handles loading/error/fallback states.
- Pipeline can be rerun from documented commands.
- Model artifacts can be regenerated or loaded predictably.

## Error Handling

Data pipeline:

- Missing fields should be logged and handled with clear defaults.
- Too-small filtered datasets should trigger explicit warnings.

API:

- Invalid user preference payloads should return clear validation errors.
- Missing model artifacts should return service-unavailable style errors with setup guidance.
- LLM/RAG failures should not block recommendation results.

Frontend:

- Show retry actions for API failures.
- Show structured model/evidence results even when generated prose is unavailable.
- Avoid blank states.

## Architecture

High-level components:

- `frontend`: Next.js app.
- `api`: FastAPI service.
- `notebooks`: EDA and model exploration.
- `src/pipeline`: data preparation, feature extraction, training, evaluation.
- `src/models`: recommender and NLP model code.
- `src/retrieval`: review evidence indexing and lookup.
- `artifacts`: generated model/index files, ignored by git.
- `docs`: specs, diagrams, README support materials.

Data flow:

1. Public dataset is downloaded into `data/raw/`.
2. Pipeline filters and preprocesses data into `data/processed/`.
3. NLP feature extraction creates product profiles and evidence snippets.
4. Recommender training creates model artifacts.
5. FastAPI loads artifacts and serves recommendation/report endpoints.
6. Next.js calls FastAPI and renders the report-first workspace.
7. Portfolio materials summarize the process and outcomes.

## Testing Strategy

Pipeline tests:

- Validate preprocessing on small fixture data.
- Validate model input/output shapes.
- Validate metric calculations.

API tests:

- Health endpoint.
- Recommendation request/response schema.
- Report fallback when explanation generation fails.
- Compare endpoint for known product ids.

Frontend tests:

- Preference form validation.
- Report rendering with mock API response.
- Error and loading states.
- Responsive layout smoke checks.

Manual QA:

- Run the complete demo flow.
- Confirm report claims are connected to visible evidence.
- Confirm analysis and portfolio tabs make the project understandable to a reviewer.

## Success Criteria

Phase 1 is successful when:

- A reviewer can run or view the demo and understand the product in under two minutes.
- The recommendation report shows Top 3 products, reasons, evidence, pros/cons, and cautions.
- At least three model tiers are documented: baseline, core, advanced Two-Tower Retrieval.
- Evaluation results are summarized in GitHub and Notion.
- The repo is structured enough that another engineer can reproduce the pipeline.
- The UI follows `DESIGN.md` and feels like a finished beauty commerce AI product.

## Planning Defaults

- Dataset default: Amazon Reviews 2023 beauty-related category data, narrowed to a manageable subset during pipeline setup.
- Collaborative filtering default: explicit ratings first; implicit-feedback conversion only if needed.
- LLM default: real LLM calls in development with a deterministic fallback/mock path for demos and cost control.
- Deployment default: local-first Phase 1, with frontend deployable to Vercel and API deployable to a container-friendly host.
- Project name default: GlowFit AI.
