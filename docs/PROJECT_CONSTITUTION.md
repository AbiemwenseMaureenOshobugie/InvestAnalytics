# InvestAnalytics Project Constitution

**Status:** Foundational specification v0.1  
**Applies to:** The InvestAnalytics repository, product, architecture, data, analytics, AI, and governance work.

## 1. Purpose

InvestAnalytics is an investment intelligence and portfolio decision-support platform. The project exists to help individuals and investment professionals understand portfolios, analyze investments, investigate changes, evaluate evidence, simulate scenarios, make informed human decisions, and monitor those decisions over time.

The system is decision-support software. It is not an autonomous investment decision-maker.

## 2. Authority and source of truth

The following authority order applies:

1. The user has final product authority.
2. Approved specifications and architecture decisions committed to this repository define intended system behavior.
3. The Git repository and Git history are the source of truth for actual implementation state.
4. Automated tests and validation evidence establish whether implemented behavior satisfies its contracts.
5. Secondary development engines may inspect, propose, implement, test, and document work when authorized, but must not silently redefine approved product or architecture decisions.

When a conflict is discovered, stop and surface it rather than silently choosing a new direction.

## 3. Engineering principles

### 3.1 Deterministic before intelligent
Use deterministic, testable calculations and rules wherever the requirement can be expressed reliably in code. AI may interpret, retrieve, orchestrate, and explain those results; it must not replace authoritative calculations.

### 3.2 Evidence before narrative
Analytical and AI-generated explanations should be grounded in identifiable data, calculations, research, assumptions, and provenance.

### 3.3 Human decision authority
The platform supports investment decisions. It does not silently make or execute them on behalf of users.

### 3.4 Auditability by design
Important data, calculations, model versions, research artifacts, AI interactions, and decisions should be traceable.

### 3.5 Explicit contracts
Domain objects, APIs, data pipelines, analytics, and AI tools should have explicit interfaces and validation rules.

### 3.6 Provider abstraction
External market and fundamental data providers must be isolated behind provider-specific adapters so that canonical platform data does not become coupled to a single vendor.

### 3.7 Testability
Financial calculations, transformations, invariants, data-quality rules, integrations, and eventually AI behavior must be testable independently.

### 3.8 Security and privacy as first-class concerns
Authentication, authorization, secrets, sensitive portfolio information, research records, audit data, and organizational boundaries must be designed deliberately rather than added after core development.

### 3.9 Scope discipline
Do not build speculative features merely because they are technically interesting. Each major capability must trace to a product requirement, workflow, architectural need, or governance requirement.

## 4. AI governance

The canonical interaction pattern is:

**User → AI interface → domain/tool service → deterministic analysis → evidence → AI interpretation → human decision**

AI components must:

- use governed tools/services for authoritative data and calculations;
- distinguish retrieved facts from interpretation;
- preserve relevant provenance;
- expose uncertainty or missing evidence where material;
- avoid fabricating financial data, calculations, citations, or research conclusions;
- remain subject to system permissions and governance controls.

The initial product is not an autonomous trading bot, stock-price prediction engine, guaranteed-return system, or unrestricted autonomous agent.

## 5. Change control

A change that affects product scope, domain contracts, architecture, data ownership, analytical definitions, AI governance, security boundaries, or workflow semantics requires explicit documentation.

Major architectural decisions should be recorded as ADRs.

When proposing a change, state:

- current decision;
- problem or limitation;
- evidence;
- proposed change;
- consequences and trade-offs;
- whether user approval is required.

Do not silently overwrite another development engine's work.

## 6. Multi-engine collaboration

Before modifying the repository, a development engine should inspect:

- current branch and HEAD;
- recent commits;
- relevant specifications;
- existing implementation;
- tests and validation;
- related open work where relevant.

After modifying the repository, it should report:

- files changed;
- behavior added or changed;
- tests run and results;
- exact commit SHA;
- known limitations or unresolved issues.

## 7. Documentation standard

Documentation is part of the product engineering system. Foundational product, domain, architecture, data, analytics, AI, governance, and operational decisions should be versioned in the repository.

Prefer concise, explicit documentation over informal assumptions held only in conversation.

## 8. Delivery sequence

The intended strategic sequence is:

- **IA-0 — Foundation:** product architecture, domain model, security model, data architecture, development standards, governance.
- **IA-1 — Equity Intelligence Core:** securities, markets, prices, corporate actions, fundamentals, portfolios, transactions.
- **IA-2 — Portfolio Analytics:** valuation, performance, attribution, allocation, benchmarking.
- **IA-3 — Risk Intelligence:** volatility, drawdown, correlation, concentration, VaR, Expected Shortfall, stress testing.
- **IA-4 — Investment Research:** research objects, thesis, evidence, assumptions, invalidation conditions.
- **IA-5 — Monitoring:** change detection, thesis monitoring, alerts, risk monitoring.
- **IA-6 — AI Analyst:** natural language, tool use, evidence retrieval, reasoning, explainability.
- **IA-7 — Professional Platform:** organizations, permissions, collaboration, committees, reporting, audit.
- **IA-8 — Multi-Asset Expansion:** ETFs, fixed income, FX, commodities, funds, derivatives, and other supported assets.

The sequence may change only through an explicit, documented architectural/product decision.

## 9. Initial technology direction

Subject to validation during IA-0:

- Python for backend and quantitative analytics;
- PostgreSQL for primary relational persistence;
- FastAPI for API services;
- React + TypeScript for the web application;
- Power BI as a professional reporting/integration layer;
- GitHub and GitHub Actions for source control and CI/CD.

Libraries and infrastructure components should be introduced only when justified by requirements.

## 10. Definition of a healthy change

A healthy change is small enough to review, explicit about its contract, covered by appropriate validation, documented when consequential, and consistent with this constitution.

The constitution itself is versioned. Material changes require a documented rationale.
