# Supabase Catalog

GlowFit keeps the bundled JSON catalog as the default development source. Set
`GLOWFIT_CATALOG_SOURCE=supabase` to make the FastAPI server load products,
tags, and reviews from Supabase instead.

## Local Supabase setup

1. Start the Supabase stack with `npx supabase start`.
2. Apply the repository migration and seed with `npx supabase db reset`.
3. Copy the local API URL and legacy `service_role` key printed by the CLI into a local `.env` file
   as `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.
4. Set `GLOWFIT_CATALOG_SOURCE=supabase` in that file.
5. Set `GLOWFIT_CORS_ORIGINS=http://localhost:3000` for the local frontend.
6. Optionally set `GLOWFIT_CATALOG_CACHE_TTL_SECONDS=60` to control how often the API refreshes
   the remote catalog. A short cache avoids three Supabase reads for every recommendation request.
7. Start the API server with
   `python3 -m uvicorn api.main:app --env-file .env --reload --port 8000`.
8. Verify the configured catalog before a demo with
   `python3 scripts/verify_supabase_catalog.py --env-file .env`.

## Hosted Supabase project

1. Apply `supabase/migrations/20260710234242_create_glowfit_catalog.sql` and `supabase/seed.sql`
   to the intended project using the Supabase CLI or SQL Editor.
2. In **Settings > API Keys**, create or reveal a server-only key from **Secret keys**.
3. Set `SUPABASE_URL` and `SUPABASE_SECRET_KEY` in the API server's secret environment.
4. Set `GLOWFIT_CATALOG_SOURCE=supabase` and the deployed frontend origin in
   `GLOWFIT_CORS_ORIGINS`.
5. Run `python3 scripts/verify_supabase_catalog.py --env-file .env` from a trusted machine before
   a demo or deployment.

For an older project that only has legacy JWT keys, use the `service_role`
value as `SUPABASE_SERVICE_ROLE_KEY` instead. The repository supports both
formats, but new Secret keys are preferred.

Secret and legacy service-role keys bypass RLS and belong only in the API server environment. Do
not put either value in the frontend or any `NEXT_PUBLIC_*` variable. The browser talks only to the
FastAPI API; it does not hold a Supabase credential.

When the API cannot reach Supabase, it returns HTTP `503` and the frontend displays that state.
It does not substitute local mock recommendations for a failed remote request.

## Schema

- `products`: product catalog and aggregate quality signals
- `product_tags`: normalized attributes used by profile matching
- `reviews`: review text, rating, and review date

All tables are in the exposed `public` schema with RLS enabled. The current frontend does not
access Supabase directly, and no public read policy is created. FastAPI uses a server-only Secret
key or legacy service-role key to load the catalog.
