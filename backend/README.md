# InvestAnalytics Backend

IA-0A provides the executable backend skeleton only.

## Local setup

From the backend directory:

    python -m venv .venv
    pip install -e ".[dev]"

Copy .env.example to .env when local configuration is needed.

Run the API:

    uvicorn app.main:app --reload

Endpoints:

- GET /api/v1/health — process health.
- GET /api/v1/readiness — runtime readiness; returns 503 when PostgreSQL is not configured.

No investment-domain persistence or provider integration exists in IA-0A.
