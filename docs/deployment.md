# Deployment Checklist

## Production environment

Set these API variables in the hosting provider's secret environment. Do not commit a production
`.env` file.

```bash
GLOWFIT_ENV=production
GLOWFIT_TRUSTED_HOSTS=api.example.com
GLOWFIT_CORS_ORIGINS=https://app.example.com
GLOWFIT_CATALOG_SOURCE=supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SECRET_KEY=sb_secret_<server-only-key>
```

`GLOWFIT_TRUSTED_HOSTS` contains API hostnames only, without `https://`. Production startup fails
when it is empty. FastAPI's `/docs`, `/redoc`, and `/openapi.json` are disabled in production.

## Frontend environment

Set this value in the frontend host's build environment:

```bash
NEXT_PUBLIC_API_BASE_URL=https://api.example.com
```

It is safe to expose the API base URL, but never expose `SUPABASE_SECRET_KEY` or
`SUPABASE_SERVICE_ROLE_KEY` through a `NEXT_PUBLIC_*` variable.

## Start command

Use a non-reload command in production:

```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port "$PORT"
```

## Staging smoke checks

1. `GET /health` reports `data_source: "supabase"`.
2. `POST /recommendations` returns recommendations for a valid profile.
3. `GET /docs` returns `404` in production.
4. An untrusted `Host` is rejected.
5. The Vercel Firewall rate-limit rule returns `429` for repeated API requests.
6. The frontend response includes CSP, `X-Content-Type-Options`, `Referrer-Policy`, and frame
   protection headers.

## Provider boundary

## Vercel Hobby deployment

Deploy the frontend and API as separate Vercel projects connected to the same Git repository.
The frontend project uses `frontend` as its Root Directory. The API project uses the repository root
and must expose the FastAPI application through Vercel's Python runtime entry point.

Set `NEXT_PUBLIC_API_BASE_URL` in the frontend project to the deployed API URL. Set the API
variables above only in the API project, never in the frontend project.

In **Vercel Dashboard → Firewall → Rate Limiting**, create one rule for the API project:

| Setting | Value |
| --- | --- |
| Path | `/recommendations` |
| Threshold | 30 requests per 60 seconds per IP |
| Action | Block (`429`) |

Vercel Hobby includes a limited monthly rate-limit allowance suitable for a personal portfolio.
The limit belongs at Vercel's edge, where it sees the visitor IP correctly and is shared across
serverless instances. Do not add an in-memory application limiter as a substitute.

Cloudflare is optional until you own a custom domain. A `*.vercel.app` URL cannot be proxied through
your Cloudflare zone, so use Vercel Firewall first.
