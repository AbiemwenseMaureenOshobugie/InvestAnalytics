# InvestAnalytics backend

The backend is a Python 3.11 modular monolith.

## IA-1C persistence

IA-1C Batch 2 introduces the first real persistence boundary:

- PostgreSQL via SQLAlchemy Core and psycopg;
- version-controlled Alembic migrations;
- S3-compatible raw-artifact storage via boto3;
- provider-neutral repository adapters;
- real-service integration tests.

Domain and application packages remain independent of SQLAlchemy, PostgreSQL drivers, boto3, and provider SDKs.

### Local integration services

Set DATABASE_URL and the RAW_STORAGE_* settings, then build the schema with:

    cd backend
    alembic upgrade head
    pytest

Ordinary unit tests do not require external services. The IA-1C integration suite skips locally when the real services are not configured, but CI fails if the required integration environment is missing.
