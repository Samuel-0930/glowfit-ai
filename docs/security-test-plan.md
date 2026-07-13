# Security Test Plan

## Purpose

This plan turns the current threat model into regression tests. It is deliberately split between
tests that can run in CI today and tests that require the production edge or a real Supabase project.
It does not claim that application tests alone provide rate limiting, WAF, or secret-management
protection.

## CI Tests To Add First

### 1. Request-boundary validation — implemented

**Risk:** Anonymous callers can send oversized preference fields or unbounded comparison lists.

The API now constrains the profile vocabulary, preference term length, preference list size, budget,
and comparison product IDs. API tests assert a `422` response for invalid enum values, oversized
preference lists, and oversized comparison requests. Continue adding boundary pairs whenever the
product contract changes.

- `skin_type`, `texture`, and `fragrance_sensitivity` values outside the supported vocabulary.
- concern and avoid arrays with more items than the product contract allows.
- individual concern and avoid values longer than the accepted limit.
- `/compare` payloads with more product IDs than the configured maximum.
- malformed JSON and an unsupported `Content-Type`.

**Implementation prerequisite:** Add explicit Pydantic field constraints to `UserPreferences` and a
request model for `/compare`. Keep test values just below and just above each boundary.

### 2. CORS allowlist regression — implemented

**Risk:** A configuration change accidentally allows an untrusted browser origin.

Tests now assert that:

- the configured frontend origin receives `access-control-allow-origin` on preflight;
- an unlisted origin receives no allow-origin response;
- credentials remain disabled;
- comma-separated origins with whitespace are normalized correctly.

The origin parser is also tested directly to keep whitespace normalization deterministic.

### 3. Catalog outage and error minimization

**Risk:** Supabase outages expose internal errors or are mistaken for successful recommendations.

Extend the existing `503` test to cover `URLError`, timeout, and HTTP error inputs. Assert that the
response contains a Korean user-safe message, excludes URLs, key fragments, and stack traces, and
never returns recommendations. The frontend already verifies that a failed request shows an alert
instead of mock recommendations; keep that test as a regression guard.

### 4. Server-key boundary — partially implemented

**Risk:** A server credential reaches the browser bundle or legacy/new key handling regresses.

CI now scans browser source directories for `SUPABASE_SECRET_KEY`, `SUPABASE_SERVICE_ROLE_KEY`,
and `sb_secret_`. Catalog tests already confirm that modern Secret keys never produce an
`Authorization` header and legacy keys do. Keep configuration documentation outside this scan so
environment variable names remain documentable without allowing actual key values.

## Integration Tests For Supabase

### 5. Least-privilege catalog contract

**Risk:** The API reads or returns fields that are unnecessary for recommendation delivery.

Against a disposable local Supabase stack or dedicated test project, verify that:

- RLS is enabled on all three catalog tables;
- `anon` and `authenticated` cannot select the catalog tables without a policy;
- the server credential can read only the fields used by the API;
- API responses never contain `user_id`, API keys, or database error detail;
- a migration plus seed can be applied twice without failure.

The final item should be a database integration test, not merely SQL string inspection.

### 6. Remote catalog failure behavior

**Risk:** Expiry of the cache causes slow or inconsistent API behavior.

Use a controllable HTTP stub or test Supabase project to verify that a warm cache avoids repeated
table reads inside the TTL, then that an expired cache refreshes exactly once. Simulate a timeout and
assert a bounded `503` response. Track request latency so the API does not serially wait for three
long timeouts.

## Deployment Tests

### 7. Public edge controls — application baseline implemented

**Risk:** Application-level tests cannot prove that a public deployment is protected from abuse.

The application disables OpenAPI/docs in `GLOWFIT_ENV=production`, requires configured trusted
hosts before starting production, and sends browser security headers from Next.js. Production rate
limiting is configured in Vercel Firewall so it is applied before the serverless function and is
shared across instances.

In a staging environment, run authenticated smoke checks for the agreed deployment policy:

- request body limit and per-IP rate limit return `413` and `429` respectively;
- API docs are disabled or protected in production;
- `Host` validation rejects an untrusted host;
- HTTPS responses include the chosen CSP, `frame-ancestors`, `X-Content-Type-Options`, and
  `Referrer-Policy` headers;
- production does not run with `--reload`.

Store only pass/fail evidence and header names in CI artifacts. Do not log secrets, full review text,
or real user preference payloads.

### 8. Future review privacy gate

**Risk:** Raw review text may contain personal information when real reviews are introduced.

Before accepting external reviews, add a test corpus with names, email addresses, phone numbers,
order numbers, and health-related text. Assert that the public evidence DTO uses a moderated,
length-capped display excerpt and never returns direct identifiers. This is a release-blocking gate
for any user-submitted review feature.

## Execution Order

1. Add request-boundary, CORS, outage, and secret-boundary tests with the accompanying API hardening.
2. Run the Supabase integration suite on every migration or catalog-query change.
3. Add staging edge tests before public deployment.
4. Make the review privacy gate mandatory before collecting real-user reviews.
