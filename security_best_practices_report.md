# GlowFit AI Security Best-Practices Review

**Scope:** FastAPI API, Next.js client, Supabase catalog integration, data-ingestion scripts, and CI configuration in this repository.  
**Review date:** 2026-07-12  
**Context used:** portfolio/demo service today; public deployment and real user reviews are planned later. No secrets were read or included.

## Executive summary

The current JSON-backed portfolio demo has a small attack surface and no evident code-execution, SQL-injection, or client-side HTML-injection sink. The material risks arise when it is publicly hosted or switched to the Supabase catalog: the API is deliberately public and unauthenticated, has no visible request-abuse controls, and returns verbatim review evidence. That is acceptable only for a small static/demo dataset behind platform-level protections; it must be hardened before collecting real reviews or exposing a public API.

## Findings

### SBP-001 — Public API has no request-abuse controls

- **Severity:** High for an internet-facing deployment; Medium for a portfolio deployment protected by an upstream CDN/WAF.
- **Location:** `api/main.py:87-170` (`/health`, `/products`, `/recommend`, `/recommendations`, `/report`, `/compare`); `api/main.py:50-61`.
- **Evidence:** Every route is reachable without an authentication dependency, and no application-side rate limit, request-body limit, or concurrency limit is configured. `RecommendationRequest.limit` is bounded at `api/main.py:26-29`, but its nested preference strings/lists are not bounded.
- **Impact:** An anonymous client can repeatedly trigger catalog reads and ranking work, enumerate the entire product catalog through `GET /products`, and send large JSON bodies to consume API or database capacity.
- **Fix:** Put the deployed API behind a CDN/WAF or reverse proxy with per-IP rate limits, body-size limits, request timeouts, and concurrency limits. Add Pydantic `max_length`/`max_items` constraints to `UserPreferences` at `src/glowfit/schemas.py:26-32`; cap `/compare` IDs and decide whether `/products` needs pagination or should remain public.
- **False-positive/verification note:** If the chosen hosting platform already enforces these limits, document their exact values and add a regression check. CORS at `api/main.py:51-61` is not an access-control mechanism.

### SBP-002 — Recommendation responses disclose raw review text

- **Severity:** High once real user reviews are stored; Low for the current public/sample dataset.
- **Location:** `src/glowfit/evidence.py:34-43`, `src/glowfit/schemas.py:35-51`, `api/main.py:128-149`.
- **Evidence:** `EvidenceIndex.search()` copies `review.text` directly into every `EvidenceSnippet`, and `/recommendations` returns the recommendations including those snippets.
- **Impact:** Free-text reviews can contain names, email addresses, phone numbers, order details, or other identifying information. A public recommendation endpoint can then disclose that content without requiring an account. The current response does not expose `user_id`, which is good, but that does not remove the free-text risk.
- **Fix:** Before accepting real reviews, define a data-minimization policy: do not return raw review text by default; store/serve a moderated and length-capped display excerpt; remove direct identifiers; and require review ownership/consent rules. Run PII detection/redaction and establish deletion/retention handling. Keep `user_id` out of all response models.
- **Defense in depth:** Make product-level evidence public only if it is explicitly intended to be public, and audit access to source reviews separately.

### SBP-003 — Server-side Supabase credential has broad read access

- **Severity:** Medium now; High if the service key, API host, or future write paths are compromised.
- **Location:** `src/glowfit/catalog.py:71-123, 126-140`; `supabase/migrations/20260710234242_create_glowfit_catalog.sql:18-36`.
- **Evidence:** The API loads `user_id`, review text, and dates using `SUPABASE_SECRET_KEY` or `SUPABASE_SERVICE_ROLE_KEY`; the migration grants the service role read access to all three catalog tables.
- **Impact:** A leaked server credential or an SSRF/configuration issue could expose all catalog records, including future user-linked reviews. Service-role credentials also bypass the protection model normally supplied by RLS.
- **Fix:** Keep the key only in managed server secrets (the repo correctly ignores `.env` at `.gitignore:2-4`). Use a dedicated least-privilege database role or a narrowly scoped RPC/view for the catalog response that omits `user_id`; rotate the key if exposure is suspected; and restrict `SUPABASE_URL` to HTTPS production endpoints in deployment validation.
- **False-positive/verification note:** The repository has no write access yet, which limits the immediate impact. Confirm Supabase's production key type, role grants, network restrictions, and rotation process.

### SBP-004 — Input schemas lack size and vocabulary bounds

- **Severity:** Medium.
- **Location:** `src/glowfit/schemas.py:26-32`; `api/main.py:128-136, 168-170`.
- **Evidence:** Preference fields are arbitrary strings and lists without maximum list sizes or string lengths; `/compare` accepts an unbounded list of IDs.
- **Impact:** Large requests can inflate JSON parsing, token matching, evidence lookup, and response work. Free-form terms also make logs and future analytics harder to control.
- **Fix:** Add explicit maximum lengths and item counts (for example, 10 concerns/avoid terms, 100 characters per term, 20 IDs for compare) and validate enumerated fields such as skin type/texture where product requirements allow it. Enforce an upstream request-body limit as well.

### SBP-005 — Production hardening is not represented in application/deployment config

- **Severity:** Medium for public deployment; Low for local demo.
- **Location:** `api/main.py:50-61`; `frontend/next.config.mjs:7-10`; `docs/supabase.md:19`.
- **Evidence:** FastAPI uses default public OpenAPI/docs routes and has no visible `TrustedHostMiddleware`; Next.js has no visible CSP, clickjacking, or MIME-sniffing headers. The documented server command includes `--reload`, appropriate locally but unsafe in production.
- **Impact:** Production metadata exposure, Host-header ambiguity, weaker browser defense-in-depth, and accidental deployment of a development server.
- **Fix:** Introduce an explicit production configuration: disable or protect API docs, configure Trusted Host handling, set a conservative CSP plus `frame-ancestors`, `X-Content-Type-Options: nosniff`, and `Referrer-Policy` at the frontend/edge, and provide a non-reload production start command. Do not set HSTS until the final HTTPS/domain deployment is known.

### SBP-006 — Dependency and CI security checks are absent

- **Severity:** Low now; Medium as the project becomes maintained or publicly deployed.
- **Location:** `pyproject.toml:6-19`; `frontend/package.json`; `.github/workflows/ci.yml:1-45`.
- **Evidence:** Python dependencies use open lower bounds without a lockfile; CI runs lint/tests/build but no dependency vulnerability scan, SBOM, or pinned-action commit SHAs.
- **Impact:** Vulnerable transitive packages or a compromised action release can reach builds unnoticed.
- **Fix:** Add a dependency scanning step (for Python and npm), generate/retain dependency lock data, and consider pinning GitHub Actions to reviewed commit SHAs. Keep upgrades deliberate and tested.

## Positive controls observed

- `.env` files are ignored and `.env.example:6-13` explicitly forbids exposing Supabase keys to `NEXT_PUBLIC_*` variables.
- The browser calls only the FastAPI API; direct Supabase frontend access is intentionally not enabled (`docs/supabase.md:39-41`).
- CORS is an explicit allowlist with credentials disabled (`api/main.py:51-61`), rather than wildcard credentials.
- Responses are modeled with Pydantic, and `limit` is bounded (`api/main.py:26-29`).
- No `dangerouslySetInnerHTML`, direct DOM HTML sink, shell execution, dynamic evaluation, upload handler, or SQL string construction was found in the reviewed runtime paths.

## Recommended implementation order

1. Before any public deployment: enforce edge rate/body limits; bound API schemas; add production headers/host configuration; disable/protect docs.
2. Before real user reviews: redesign review storage and response DTOs around minimization/redaction, consent, deletion, and access policy; replace the broad service-role read with a least-privilege catalog path.
3. Before ongoing public maintenance: add dependency scanning and a documented production deployment configuration.

