# IA-0A Implementation Skeleton Specification

**Version:** 0.1  
**Status:** Approved implementation specification  
**Product:** InvestAnalytics

## 1. Purpose

IA-0A establishes the minimum executable repository structure required to begin implementation without prematurely implementing unresolved investment-domain behavior.

It operationalizes the approved System Architecture Specification while deliberately leaving final domain schemas, provider choices, authentication implementation, analytical methodologies, and AI behavior for later milestones.

## 2. IA-0A scope

IA-0A establishes:

- Python backend project structure;
- domain/application/infrastructure/interface boundaries;
- frontend boundary;
- configuration foundation;
- test structure;
- API bootstrap;
- health/readiness endpoints;
- CI foundation;
- dependency and quality tooling;
- basic database connectivity abstraction without domain tables;
- clear local-development conventions.

IA-0A does **not** implement:

- portfolio workflows;
- investment calculations;
- provider integrations;
- authentication provider;
- authorization policy;
- production database schema;
- AI analyst behavior;
- Power BI integration;
- market/fundamental ingestion;
- business-domain persistence.

## 3. Repository target structure

The initial repository should converge toward:

```text
InvestAnalytics/
├── backend/
│   ├── app/
│   │   ├── domain/
│   │   │   ├── portfolio/
│   │   │   ├── reference_data/
│   │   │   ├── market_data/
│   │   │   ├── fundamentals/
│   │   │   ├── performance/
│   │   │   ├── risk/
│   │   │   ├── research/
│   │   │   ├── thesis/
│   │   │   ├── monitoring/
│   │   │   ├── scenario/
│   │   │   ├── reporting/
│   │   │   ├── decisions/
│   │   │   ├── governance/
│   │   │   └── ai/
│   │   ├── application/
│   │   │   ├── portfolio/
│   │   │   ├── reference_data/
│   │   │   ├── market_data/
│   │   │   ├── fundamentals/
│   │   │   ├── analytics/
│   │   │   ├── research/
│   │   │   ├── monitoring/
│   │   │   ├── scenario/
│   │   │   ├── reporting/
│   │   │   ├── decisions/
│   │   │   ├── ai/
│   │   │   └── governance/
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   ├── providers/
│   │   │   ├── http/
│   │   │   ├── auth/
│   │   │   ├── jobs/
│   │   │   ├── storage/
│   │   │   ├── ai/
│   │   │   ├── observability/
│   │   │   └── cache/
│   │   └── interfaces/
│   │       ├── api/
│   │       └── workers/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── data_quality/
│   │   ├── invariants/
│   │   └── end_to_end/
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   └── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
└── README.md
```

Exact package names may be refined during implementation, but the dependency boundaries are mandatory.

## 4. Backend bootstrap

The backend must expose a minimal application factory/runtime entry point.

The bootstrap must:

1. load validated configuration;
2. construct the application;
3. register API routes;
4. expose health/readiness endpoints;
5. initialize only infrastructure required for the requested runtime;
6. avoid importing unresolved domain implementations merely to start the service.

The application must be startable locally before any investment-domain feature exists.

## 5. Health and readiness

Two distinct concepts should be established:

### Health

Answers whether the application process is alive and able to serve basic requests.

### Readiness

Answers whether required runtime dependencies for normal service operation are available.

The readiness contract must be explicit about dependency failures. A database connectivity failure should not be represented as healthy readiness.

These endpoints must contain no sensitive configuration or credentials.

## 6. Configuration

Configuration must be centralized and typed.

At minimum, establish concepts for:

- application environment;
- application name/version;
- API settings;
- database connection configuration;
- logging level;
- allowed frontend origins;
- feature/configuration flags.

Secrets must be loaded from environment/runtime secret mechanisms, never committed.

Configuration should fail clearly when required values are malformed.

## 7. Dependency management

Python dependencies must be declared through the project package configuration.

Dependencies should be grouped conceptually as:

- runtime;
- development/testing.

IA-0A should keep runtime dependencies minimal.

FastAPI and the selected ASGI server are implementation dependencies for the API boundary. Exact database/ORM dependencies should not be added merely to create empty domain tables.

## 8. Domain package rules

Domain packages may contain only domain concepts and contracts required at this stage.

IA-0A should initially create package boundaries and minimal placeholder documentation/tests rather than inventing entities.

Domain packages must not import:

- FastAPI;
- SQLAlchemy/ORM implementation;
- provider SDKs;
- HTTP clients;
- frontend code;
- model-provider SDKs.

## 9. Application package rules

Application packages contain use-case orchestration contracts.

IA-0A may establish shared abstractions such as:

- request context;
- result/error conventions;
- repository ports;
- service interfaces.

No investment workflow should be implemented yet unless required solely to prove the skeleton.

## 10. Infrastructure package rules

Infrastructure establishes adapters and configuration boundaries without binding the product to unresolved providers.

The persistence boundary should expose a database connection/session abstraction suitable for later repository implementation.

No portfolio, transaction, security, market observation, thesis, report, or decision tables should be created in IA-0A.

## 11. API boundary

The API should initially expose only infrastructure/bootstrap endpoints such as:

- health;
- readiness.

A versioned API namespace may be established without adding business resources.

Route handlers must remain thin and must not contain domain logic.

## 12. Frontend boundary

The frontend directory should establish the React + TypeScript application boundary.

IA-0A should prove that the frontend can:

- build;
- run locally;
- communicate with the backend health endpoint where appropriate.

No investment dashboard or portfolio UI should be built yet.

## 13. Testing foundation

At minimum, IA-0A must establish:

- backend unit-test execution;
- API smoke tests;
- configuration tests;
- import/package-boundary sanity checks;
- frontend build/test command where the frontend scaffold supports it.

The initial test suite should prove that:

- the backend starts;
- health responds successfully;
- readiness behaves according to configured dependencies;
- invalid configuration fails predictably;
- the project can be tested in CI.

## 14. CI foundation

GitHub Actions should run on relevant pushes and pull requests.

Initial CI stages:

1. repository checkout;
2. Python environment setup;
3. dependency installation;
4. formatting/lint checks;
5. static/type checks where configured;
6. backend tests;
7. frontend dependency installation/build/test;
8. basic artifact/status reporting.

CI must fail on broken tests or configured quality checks.

Provider credentials and production secrets must never be required for basic CI.

## 15. Database boundary

IA-0A establishes connectivity infrastructure only.

The architecture should support:

**Application → Repository Port → Persistence Adapter → PostgreSQL**

No domain schema is required yet.

If a local PostgreSQL service is not available, backend startup should remain possible in a mode that does not require database access, while readiness accurately reports database unavailability.

The exact ORM and migration tooling remain deferred unless implementation evidence requires choosing them during IA-0.

## 16. Dependency-direction verification

IA-0A should include automated or reviewable checks that prevent obvious architectural violations.

At minimum, verify:

- domain does not import infrastructure;
- domain does not import API frameworks;
- application does not depend on provider SDKs;
- API does not directly access persistence implementations;
- frontend does not access PostgreSQL/provider credentials.

The exact enforcement mechanism may be implemented later if static architecture tooling is not justified yet.

## 17. Local development

Provide a concise developer workflow covering:

1. install dependencies;
2. configure environment;
3. run backend;
4. run backend tests;
5. run frontend;
6. run CI-equivalent checks locally.

Local development must not require production credentials.

## 18. Documentation

IA-0A should add or update:

- backend README;
- frontend README;
- environment/configuration example;
- developer setup instructions;
- architecture navigation in the root README if needed.

Documentation must distinguish placeholders from implemented capabilities.

## 19. Acceptance criteria

IA-0A is complete when:

- the repository contains the approved architectural package boundaries;
- backend starts successfully;
- health endpoint works;
- readiness endpoint has defined dependency behavior;
- configuration is typed and validated;
- secrets are excluded from source control;
- backend tests run;
- frontend scaffold builds;
- CI executes successfully;
- database connectivity has a clean infrastructure boundary;
- no domain schema has been invented prematurely;
- no provider has been coupled into the domain;
- dependency direction is preserved;
- documentation explains local setup;
- all changes are committed with a clear message.

## 20. Implementation constraints

During IA-0A:

- do not rewrite Git history;
- do not alter existing foundational specification documents without an explicit architectural reason;
- do not add speculative business entities;
- do not implement fake market data;
- do not add an AI chatbot merely to demonstrate AI;
- do not select providers merely because they are convenient;
- do not create microservices;
- do not introduce infrastructure whose operational complexity is not justified;
- do not make unrecorded architectural decisions.

## 21. Next step

Once this specification is accepted and committed, implementation may proceed to the actual repository/application skeleton.

The implementation should be incremental and verified after each meaningful boundary is introduced.
