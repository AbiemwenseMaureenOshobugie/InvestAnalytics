# InvestAnalytics

**Investment Intelligence & Portfolio Decision-Support Platform for Nigerian and global equities.**

InvestAnalytics is a governed investment analytics platform designed for individual investors and professional investment workflows.

## Current status

**IA-0A implementation in progress — executable application skeleton established.**

The repository now contains the initial backend/frontend boundaries, typed configuration, FastAPI bootstrap, health/readiness endpoints, PostgreSQL connectivity boundary, backend tests, frontend scaffold, and GitHub Actions CI foundation.

Business-domain workflows, persistence schema, data providers, authentication, investment calculations, and AI analyst behavior are intentionally not implemented yet.

## Product loop

**Observe → Analyze → Explain → Investigate → Simulate → Decide → Monitor → Observe**

## Initial scope

- **Asset class:** Equities
- **Markets:** Nigeria + global
- **Users:** Individual investors + professional investment workflows

## Architecture

The approved architecture is a governed modular monolith with explicit domain/application/infrastructure boundaries.

- [Project Constitution](docs/PROJECT_CONSTITUTION.md)
- [Product Charter](docs/PRODUCT_CHARTER.md)
- [Master Context](docs/MASTER_CONTEXT.md)
- [Workflow Specification](docs/USER_SYSTEM_WORKFLOW_SPECIFICATION.md)
- [Domain Model Specification](docs/DOMAIN_MODEL_SPECIFICATION.md)
- [System Architecture Specification](docs/SYSTEM_ARCHITECTURE_SPECIFICATION.md)
- [IA-0A Implementation Skeleton Specification](docs/IA-0A_IMPLEMENTATION_SKELETON_SPECIFICATION.md)

## Local development

Backend:

    cd backend
    python -m venv .venv
    pip install -e ".[dev]"
    uvicorn app.main:app --reload

Frontend:

    cd frontend
    npm install
    npm run dev

## Architectural principle

AI is an assistant over governed domain services and deterministic analytics:

**User → AI interface → domain/tool service → deterministic analysis → evidence → AI interpretation → human decision**

InvestAnalytics is not initially an autonomous trading system, stock-price prediction engine, guaranteed-return system, or generic financial chatbot.
