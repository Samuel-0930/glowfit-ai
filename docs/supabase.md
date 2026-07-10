# Supabase Catalog

GlowFit keeps the bundled JSON catalog as the default development source. Set
`GLOWFIT_CATALOG_SOURCE=supabase` to make the FastAPI server load products,
tags, and reviews from Supabase instead.

## Local setup

1. Start the Supabase stack with `npx supabase start`.
2. Apply the repository migration and seed with `npx supabase db reset`.
3. In Supabase Dashboard, open **Settings > API Keys** and create or reveal a
   key in the **Secret keys** section.
4. Register the project API URL and that key in a local `.env` file as
   `SUPABASE_URL` and `SUPABASE_SECRET_KEY`.
5. Set `GLOWFIT_CATALOG_SOURCE=supabase` in that file.
6. Start the API server with `uvicorn api.main:app --env-file .env --reload --port 8000`.

For an older project that only has legacy JWT keys, use the `service_role`
value as `SUPABASE_SERVICE_ROLE_KEY` instead. The repository supports both
formats, but new Secret keys are preferred.

Secret and service-role keys belong only in the API server environment. Do not
put either value in the frontend or any `NEXT_PUBLIC_*` variable.

## Schema

- `products`: product catalog and aggregate quality signals
- `product_tags`: normalized attributes used by profile matching
- `reviews`: review text, rating, and review date

All tables are in the exposed `public` schema with RLS enabled. The current
frontend does not access Supabase directly; the FastAPI server reads through a
service-role key, so no public read policy is created.
