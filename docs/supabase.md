# Supabase Catalog

GlowFit keeps the bundled JSON catalog as the default development source. Set
`GLOWFIT_CATALOG_SOURCE=supabase` to make the FastAPI server load products,
tags, and reviews from Supabase instead.

## Local setup

1. Start the Supabase stack with `npx supabase start`.
2. Apply the repository migration and seed with `npx supabase db reset`.
3. Copy the local API URL and service-role key into a local `.env` file.
4. Set `GLOWFIT_CATALOG_SOURCE=supabase` before starting the API server.

The service-role key belongs only in the API server environment. Do not put it
in the frontend or any `NEXT_PUBLIC_*` variable.

## Schema

- `products`: product catalog and aggregate quality signals
- `product_tags`: normalized attributes used by profile matching
- `reviews`: review text, rating, and review date

All tables are in the exposed `public` schema with RLS enabled. The current
frontend does not access Supabase directly; the FastAPI server reads through a
service-role key, so no public read policy is created.
