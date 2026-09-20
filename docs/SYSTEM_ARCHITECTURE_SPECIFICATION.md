# InvestAnalytics System Architecture Specification

**Version:** 0.1  
**Status:** IA-0 architectural specification  
**Product:** InvestAnalytics  
**Repository:** `AbiemwenseMaureenOshobugie/InvestAnalytics`

## 1. Purpose

This specification defines the initial system architecture for InvestAnalytics. It translates the approved product, workflow, and domain specifications into implementation-oriented boundaries without prematurely defining database tables, Python classes, API endpoints, or provider-specific contracts.

The architecture must support a serious, scalable, governable investment intelligence and portfolio decision-support platform while preserving the project's central principles:

- deterministic before intelligent;
- evidence before narrative;
- human decision authority;
- auditability by design;
- explicit contracts;
- provider abstraction;
- testability;
- security and privacy as first-class concerns;
- scope discipline.

This document is the architectural bridge between the domain model and the eventual implementation skeleton.

## 2. Architectural authority

The architecture derives from:

1. Project Constitution;
2. Product Charter;
3. Master Context;
4. User & System Workflow Specification;
5. Domain Model Specification.

Where an implementation choice is not required by those documents, this specification should prefer the least complex design that preserves the required contracts.

A conflict between this specification and an approved higher-level product/domain decision must be surfaced and resolved explicitly. Architecture must not silently redefine domain meaning.

## 3. Architectural goals

The initial architecture must provide:

- clear separation of domain, application, and infrastructure concerns;
- explicit logical service boundaries;
- deterministic analytical computation;
- provider-independent canonical data;
- temporal and provenance-aware data handling;
- secure portfolio, research, and decision access;
- reproducible analytical execution;
- governed AI tool use;
- asynchronous execution where work is long-running or scheduled;
- API access for the web application and approved integrations;
- reporting integration without coupling the domain to Power BI;
- strong automated testing;
- observable and auditable operations;
- a path from modular monolith to separately deployed services only when justified.

The architecture should avoid:

- premature microservices;
- provider-specific domain models;
- AI-owned financial calculations;
- direct database access from presentation code;
- hidden business logic in API handlers;
- mutable overwriting of material historical artifacts;
- ungoverned AI access to internal data;
- coupling Power BI to transactional domain persistence.

## 4. Architectural style

### 4.1 Initial deployment style

InvestAnalytics should begin as a **modular monolith** with explicit internal boundaries.

The modular monolith is the initial deployment strategy, not the conceptual service model. Logical services remain identifiable and independently testable even when they execute inside one application deployment.

This is preferred at IA-0 because:

- the product is still establishing its core domain contracts;
- transactional consistency is important;
- deployment complexity should remain low;
- the domain boundaries can be validated through real workflows before service extraction;
- premature distributed systems introduce operational complexity without a demonstrated need.

The architecture must therefore make service extraction possible without requiring the first implementation to become microservices.

### 4.2 Logical service boundaries

The initial logical capabilities are:

1. Portfolio Service
2. Reference Data Service
3. Market Data Service
4. Fundamental Data Service
5. Performance Analytics Service
6. Risk Analytics Service
7. Research Service
8. Thesis Service
9. Monitoring/Intelligence Service
10. Scenario Service
11. Reporting Service
12. Decision Service
13. AI Orchestration Service
14. Governance/Audit Service

These are capability boundaries. They are not automatically separate deployable applications.

### 4.3 Boundary rule

Each logical service owns its domain behavior and exposes application-level operations through explicit interfaces.

Other modules must not reach through a service boundary to manipulate its persistence structures directly.

## 5. Layered architecture

The application is organized into three principal layers.

### 5.1 Domain layer

Owns:

- entities and value concepts;
- domain invariants;
- state transitions;
- domain services;
- business semantics;
- analytical semantics;
- research/thesis semantics;
- decision semantics;
- domain events.

The domain layer must not depend on FastAPI, PostgreSQL, ORM implementation, provider SDKs, HTTP clients, model-provider SDKs, or UI frameworks.

### 5.2 Application layer

Owns:

- use-case orchestration;
- authorization decisions at use-case boundaries;
- transaction boundaries;
- domain-service invocation;
- repository interfaces;
- provider coordination;
- analytical execution orchestration;
- report composition;
- AI tool orchestration;
- scheduling/job coordination;
- application-level event handling.

The application layer coordinates work but must not become the authoritative home for domain rules that belong in the domain layer.

### 5.3 Infrastructure layer

Owns:

- PostgreSQL persistence;
- ORM/database adapters;
- HTTP clients;
- market/fundamental provider adapters;
- file/object storage;
- queues and job infrastructure;
- authentication integration;
- AI model-provider clients;
- caching;
- observability integrations;
- deployment/runtime concerns.

Infrastructure implementations satisfy interfaces defined by inner layers where dependency inversion is appropriate.

## 6. Dependency direction

The preferred dependency direction is:

**Interface / API → Application → Domain**

and:

**Infrastructure → Application/Domain contracts**

Infrastructure may implement ports defined by the application or domain, but domain code must not import infrastructure implementations.

The frontend communicates with backend application interfaces through documented APIs. It must not connect directly to PostgreSQL or provider APIs.

A provider adapter may depend on provider SDKs, but canonical domain/application code must not depend on provider-specific response objects.

## 7. Conceptual module structure

The implementation skeleton should eventually reflect a structure conceptually similar to:

```text
backend/
  domain/
    portfolio/
    reference_data/
    market_data/
    fundamentals/
    performance/
    risk/
    research/
    thesis/
    monitoring/
    scenario/
    reporting/
    decisions/
    governance/
    ai/

  application/
    portfolio/
    reference_data/
    market_data/
    fundamentals/
    analytics/
    research/
    monitoring/
    scenario/
    reporting/
    decisions/
    ai/
    governance/

  infrastructure/
    persistence/
    providers/
    http/
    auth/
    jobs/
    storage/
    ai/
    observability/
    cache/

  interfaces/
    api/
    workers/

frontend/
  application/
  features/
  shared/
  api/
  state/
  components/

tests/
  unit/
  integration/
  data_quality/
  invariants/
  end_to_end/
```

This is a conceptual package boundary, not a final Python package contract. Exact names may be refined during implementation.

## 8. Service interface principles

Logical services should expose explicit application interfaces such as:

- commands for state-changing operations;
- queries for retrieval and analysis;
- calculation requests for deterministic analytics;
- ingestion operations for external observations;
- monitoring evaluations;
- report composition/finalization operations;
- decision recording operations;
- governed AI tool operations.

Interfaces should make important temporal context, authorization context, input scope, and calculation methodology explicit where relevant.

Services should return typed domain/application results rather than provider-specific payloads.

## 9. API architecture

### 9.1 Backend API

FastAPI is the current technology direction for the backend API, subject to implementation validation.

The API layer is an adapter over application use cases. Route handlers should remain thin.

A typical request path is:

**HTTP request → authentication → authorization/context resolution → request validation → application use case → domain services → repositories/providers → result → response mapping**

### 9.2 API responsibilities

The API layer should handle:

- transport concerns;
- request/response schemas;
- authentication integration;
- request correlation;
- authorization handoff;
- input validation;
- error mapping;
- pagination/filter transport;
- API versioning;
- serialization.

It should not contain core portfolio, analytics, thesis, or decision logic.

### 9.3 API versioning

Publicly exposed APIs should use explicit versioning once external compatibility matters.

Internal application interfaces should not be forced to mirror HTTP resource shapes.

API schemas must not become the domain model by accident.

### 9.4 Error semantics

Errors should distinguish at least:

- invalid input;
- unauthorized access;
- forbidden access;
- missing resource;
- invalid domain state;
- unavailable/stale data;
- provider failure;
- calculation failure;
- asynchronous job state;
- unexpected internal failure.

Financially material errors must not be hidden by generic success responses.

## 10. Persistence architecture

### 10.1 Primary persistence

PostgreSQL is the current primary relational persistence direction.

It is appropriate for:

- portfolios;
- transactions;
- positions/state;
- reference data;
- observations;
- research artifacts;
- thesis versions;
- monitoring definitions/results;
- scenarios;
- reports;
- decisions;
- provenance;
- audit records;
- analytical metadata.

The database schema must be derived from domain and application contracts rather than the other way around.

### 10.2 Persistence boundary

Only infrastructure persistence adapters should communicate directly with PostgreSQL.

Domain and application services consume repository or persistence ports.

No frontend component, API route, AI tool, or provider adapter should bypass those boundaries to write domain data.

### 10.3 Historical integrity

Material historical artifacts should be versioned or immutable as defined by domain rules.

Examples include:

- thesis versions;
- report versions;
- investment decisions;
- calculation provenance;
- audit records.

Corrections must preserve historical traceability.

### 10.4 Transactions

Database transactions should protect operations that require atomic domain state changes.

Transaction boundaries belong primarily to the application layer.

Long-running analytics or provider ingestion should not hold database transactions open unnecessarily.

## 11. Data architecture

The canonical external-data path is:

**Provider → Raw Data → Validation → Normalization → Canonical Data Model → Analytics**

### 11.1 Provider adapters

Each external provider must be isolated behind an adapter implementing a common application-facing contract.

Provider adapters own:

- authentication with the provider;
- provider-specific request construction;
- provider-specific response parsing;
- provider identifiers;
- provider error handling;
- provider rate-limit handling.

They must not define the canonical InvestAnalytics domain model.

### 11.2 Raw data

Raw provider payloads should remain distinguishable from canonical data.

Where retention is justified, raw payloads should be stored with:

- provider;
- retrieval timestamp;
- request/context metadata;
- external identifiers;
- checksum/content identity where practical;
- ingestion status.

Raw data retention policy is deferred and must account for licensing and storage constraints.

### 11.3 Validation

Validation occurs before data becomes authoritative analytical input.

Validation should cover applicable:

- schema validity;
- identifier resolution;
- timestamps;
- numeric ranges;
- currency;
- duplicates;
- missingness;
- temporal consistency;
- corporate-action consistency;
- provider-specific quality indicators.

Rejected or quarantined observations must not silently enter authoritative analytics.

### 11.4 Normalization

Normalization maps provider-specific structures into canonical concepts.

Examples:

- security identifiers;
- listings;
- market observations;
- financial statements;
- fundamentals;
- corporate actions.

Normalization must preserve source/provenance information.

### 11.5 Canonical data

Canonical data is the stable platform-facing representation consumed by analytics and research services.

Analytics must operate on validated canonical inputs wherever applicable.

## 12. Temporal architecture

Investment analytics requires explicit temporal semantics.

The architecture should distinguish, where relevant:

- observation/effective time;
- retrieval/availability time;
- reporting period;
- analysis as-of time;
- decision time.

The system must avoid using information that was not available at the relevant analysis or decision time when temporal integrity matters.

An analysis request should carry sufficient as-of context to make its information boundary explicit.

## 13. Analytics execution architecture

### 13.1 Deterministic authority

Performance, attribution, risk, exposure, valuation, and scenario calculations must be performed by deterministic analytical services.

AI may explain these results but cannot replace their authoritative computation.

### 13.2 Analytics flow

A typical calculation flow is:

**Analytical Request → Input Resolution → Data Quality Check → Deterministic Calculation → Result Validation → Calculation Provenance → Analytical Result**

The result should identify:

- methodology;
- methodology/version;
- input scope;
- as-of context;
- execution time;
- relevant data-quality status;
- calculation provenance.

### 13.3 Synchronous versus asynchronous calculation

Small, bounded calculations may execute synchronously.

Long-running work should execute through a job boundary, for example:

**API → Job Request → Queue/Worker → Analytical Service → Persisted Result → Job Status**

The initial implementation may use a simple worker mechanism. A distributed queue is not required until workload justifies it.

### 13.4 Reproducibility

Material calculations should be reproducible from recorded:

- inputs or input references;
- methodology/version;
- configuration;
- as-of context;
- execution metadata.

## 14. Research architecture

Research services manage structured research artifacts rather than treating unstructured narrative as authoritative fact.

The research model should preserve:

**Thesis → Assumptions → Evidence → Monitoring**

Research records should distinguish:

- observed data;
- external evidence;
- analyst/user interpretation;
- assumptions;
- thesis statements;
- invalidation conditions.

Research content must carry appropriate provenance and version history.

## 15. Monitoring and intelligence architecture

Monitoring should operate as an evaluation system, not an autonomous decision system.

Flow:

**Monitoring Rule → Data/Research Inputs → Evaluation → Monitoring Result → Materiality Assessment → Optional Investigation → Human Attention**

Monitoring results may create investigation opportunities.

They must not silently create investment decisions or buy/sell actions.

Scheduled monitoring should run through an application job boundary rather than embedding scheduling logic inside domain entities.

## 16. Scenario architecture

Scenario analysis must be isolated from observed baseline data.

Flow:

**Baseline Context + User Assumptions + Methodology → Deterministic Scenario Engine → Scenario Result + Provenance**

Scenario inputs must be explicit and reproducible.

Scenario results must remain distinguishable from forecasts and observed outcomes.

## 17. Reporting architecture

Reporting is a composition boundary.

A report may assemble:

- portfolio state;
- performance/risk results;
- research records;
- thesis versions;
- evidence;
- scenario results;
- decision context.

Report composition should reference source artifacts and versions rather than silently copying authoritative data without traceability.

Finalized reports should be versioned or immutable according to the reporting domain contract.

AI-generated narrative may be included, but it must remain distinguishable from source facts and deterministic calculations.

## 18. AI orchestration architecture

### 18.1 Canonical AI flow

The architecture must implement:

**User → AI Interface → AI Orchestration → Governed Tool Gateway → Domain/Application Services → Deterministic Results/Evidence → AI Interpretation → User**

### 18.2 AI Orchestration Service

The AI orchestration boundary owns:

- AI request handling;
- context assembly;
- tool selection;
- tool authorization;
- tool invocation;
- result collection;
- evidence binding;
- response generation;
- interaction tracing;
- model/provider abstraction.

It does not own portfolio calculations or canonical financial facts.

### 18.3 Governed tool gateway

AI tools must be explicit, typed, permission-aware operations.

A tool should expose:

- tool identity;
- input schema;
- authorization requirements;
- allowed domain capability;
- output contract;
- provenance requirements.

The model must not receive unrestricted database or HTTP access.

### 18.4 Authorization inheritance

AI tool execution must inherit the effective authorization context of the requesting user.

A user cannot gain access to another portfolio, organization, research record, or decision through natural-language prompting.

### 18.5 Evidence binding

Tool results should retain references to the evidence/calculation/provenance used to generate the answer.

The AI response should distinguish:

- retrieved facts;
- deterministic results;
- generated interpretation;
- uncertainty or missing information.

### 18.6 Model-provider abstraction

External model providers must be isolated behind an infrastructure adapter.

Application/domain code should not depend directly on a specific model vendor.

Model name/version/configuration should be captured where governance and reproducibility require it.

## 19. Authorization and security architecture

### 19.1 Security boundary

Authentication establishes identity.

Authorization determines what that identity may access or modify.

The architecture must not treat authentication alone as sufficient protection.

### 19.2 Authorization enforcement

Authorization should be enforced at application/domain service boundaries, not only in frontend controls.

The frontend may hide unavailable actions for usability, but backend authorization remains authoritative.

### 19.3 Ownership and organization boundaries

Portfolio, research, report, and decision access must respect ownership and organization boundaries.

The exact role/permission model remains a deferred IA-0 decision, but the architecture must support:

- individual ownership;
- organization membership;
- role-based permissions;
- resource-level authorization where required.

### 19.4 Secrets

Secrets must not be committed to source control.

Provider credentials, database credentials, authentication secrets, model-provider keys, and signing material should be supplied through environment/configuration or a dedicated secrets mechanism.

## 20. Provenance and audit architecture

### 20.1 Provenance layers

The architecture recognizes:

1. Data Provenance
2. Calculation Provenance
3. Artifact Provenance
4. AI Interaction Trace
5. Audit Records

These are related but not interchangeable.

### 20.2 Data provenance

Tracks source and transformation lineage for external observations.

### 20.3 Calculation provenance

Tracks methodology, version, inputs, execution context, and quality state for analytical results.

### 20.4 Artifact provenance

Tracks author, version, source context, and history for research, thesis, scenario, report, and decision artifacts.

### 20.5 AI trace

Tracks:

**Request → context → tools → results/evidence → response**

Retention must follow privacy and governance decisions.

### 20.6 Audit records

Audit records capture material actions and state changes.

Audit records should be append-oriented and resistant to silent alteration.

Audit logs are governance records; they are not a substitute for business-domain events.

## 21. Event architecture

The domain model defines conceptual domain events.

The initial modular monolith should use an in-process application/domain event mechanism where useful.

The architecture should not require an external message broker at IA-0.

Events may be used for:

- audit capture;
- derived-state updates;
- asynchronous job requests;
- monitoring triggers;
- integration boundaries.

If future scale requires distributed events, event contracts should be versioned explicitly before extraction.

Domain events must not be confused with database change-data-capture events or log messages.

## 22. Background jobs and scheduling

Background execution is required for:

- market/fundamental data ingestion;
- scheduled monitoring;
- periodic analytics;
- report generation;
- potentially expensive scenario calculations;
- maintenance tasks.

The architecture should expose a job abstraction with:

- job type;
- input/reference;
- requested time;
- execution status;
- retry policy;
- attempt metadata;
- result/error reference.

The first implementation may use a single-process or simple worker model. A distributed task platform is deferred until operational requirements justify it.

Jobs must be idempotent where retries are possible.

## 23. Caching architecture

Caching is an optimization, not a source of financial truth.

Suitable candidates may include:

- read-heavy reference data;
- provider responses subject to safe caching rules;
- short-lived API query results;
- expensive non-authoritative computations where invalidation is well defined.

Canonical transactional state, investment decisions, audit records, and authoritative analytical provenance must not depend on an opaque cache.

Cache entries require explicit freshness semantics where financial data is involved.

## 24. Frontend architecture

React + TypeScript is the current frontend direction.

The frontend should be organized around product workflows and feature areas rather than mirroring database tables.

Likely feature areas include:

- portfolios;
- holdings/transactions;
- market/security research;
- performance;
- risk;
- thesis;
- monitoring;
- scenarios;
- reports;
- decisions;
- AI analyst;
- governance/admin.

The frontend should consume API contracts and should not embed authoritative financial calculations that duplicate backend logic.

Client-side calculations may support presentation only when clearly non-authoritative.

## 25. Power BI integration boundary

Power BI is a reporting/integration layer, not the transactional system of record.

The integration should consume governed analytical/reporting outputs rather than directly coupling Power BI to provider APIs or internal transactional tables without an approved data-access boundary.

Potential integration patterns include:

- curated analytical datasets;
- read-only reporting views;
- exported governed datasets;
- controlled API/data pipeline integration.

The exact Power BI semantic model, refresh strategy, and gateway architecture are deferred.

## 26. Observability

The system should provide structured operational telemetry covering:

- request correlation;
- job execution;
- provider calls;
- data ingestion;
- validation failures;
- calculation execution;
- AI tool invocation;
- errors;
- latency;
- resource utilization.

Observability logs must not accidentally expose sensitive portfolio data, credentials, provider secrets, or unrestricted AI prompts.

Operational logs and audit records have different purposes and retention policies.

## 27. Configuration architecture

Configuration should distinguish:

- application configuration;
- environment-specific configuration;
- secrets;
- provider configuration;
- analytics methodology configuration;
- feature flags where required.

Material analytical configuration should be versioned or captured as part of calculation provenance where it affects results.

Environment configuration must not silently change financial methodology.

## 28. Testing architecture

Testing follows the system boundaries.

### 28.1 Unit tests

Test:

- domain invariants;
- value concepts;
- state transitions;
- deterministic calculations;
- normalization rules;
- validation logic.

### 28.2 Integration tests

Test:

- PostgreSQL adapters;
- provider adapters;
- API/application boundaries;
- job execution;
- authorization enforcement;
- AI tool gateway;
- report persistence.

### 28.3 Data-quality tests

Test:

- schema validity;
- identifier resolution;
- missingness;
- duplicate handling;
- temporal consistency;
- corporate-action effects;
- provider-to-canonical mappings.

### 28.4 Invariant/property tests

Use property-based or invariant-oriented testing where useful for:

- portfolio arithmetic;
- return calculations;
- aggregation;
- risk measures;
- state transitions;
- conservation relationships.

### 28.5 End-to-end tests

Exercise complete workflows such as:

- create portfolio;
- import holdings;
- ingest market data;
- calculate performance;
- investigate change;
- research security;
- create thesis;
- monitor thesis;
- run scenario;
- generate report;
- ask AI;
- record human decision.

### 28.6 AI evaluation

AI behavior should eventually be evaluated separately for:

- tool selection;
- authorization adherence;
- evidence grounding;
- factual faithfulness;
- uncertainty handling;
- refusal to fabricate;
- response consistency.

AI tests must not replace deterministic financial calculation tests.

## 29. Deployment architecture

The initial deployment should favor a small number of independently manageable components:

- web frontend;
- backend application;
- worker/background execution;
- PostgreSQL;
- optional cache;
- optional object/file storage;
- external provider integrations;
- model-provider integrations.

A single backend deployment may host the modular domain/application services.

Deployment topology should evolve based on measured operational requirements rather than assumed scale.

## 30. Environment separation

At minimum, the architecture should support:

- local development;
- test/CI;
- staging or pre-production where practical;
- production.

Production data must not be used casually in development or automated tests.

Environment-specific credentials and configuration must be isolated.

## 31. CI/CD architecture

GitHub Actions is the current CI/CD direction.

CI should progressively enforce:

- formatting/linting;
- type checking;
- unit tests;
- integration tests where infrastructure is available;
- data-quality tests;
- migration validation;
- security checks;
- packaging/build validation.

A change that affects financial calculations or domain contracts should require appropriate automated validation before merge.

Deployment automation is deferred until the deployment target is selected.

## 32. Workflow-to-architecture traceability

| Workflow | Principal architectural path |
|---|---|
| WF-01 Create Portfolio | API → Portfolio Application Service → Portfolio Domain → PostgreSQL → Audit |
| WF-02 Add/Import Holdings | API/File Input → Import Application Service → Reference Data → Portfolio Domain → PostgreSQL → Provenance/Audit |
| WF-03 Ingest Market Data | Scheduler/Job → Provider Adapter → Validation → Normalization → Market Data Service → PostgreSQL/Raw Storage → Provenance |
| WF-04 Analyze Performance | API/Job → Performance Application Service → Portfolio/Market Data → Deterministic Analytics → Result + Calculation Provenance |
| WF-05 Investigate Performance Change | API → Investigation Service → Analytics + Research/Evidence → Investigation Result |
| WF-06 Research Security | API → Research Service → Reference/Fundamental Data + Evidence → Versioned Research Artifact |
| WF-07 Create Thesis | API → Thesis Service → Research/Evidence/Assumptions → Versioned Thesis |
| WF-08 Monitor Thesis | Scheduler/Job → Monitoring Service → Data/Research/Thesis → Monitoring Result → Investigation |
| WF-09 Run Scenario | API/Job → Scenario Service → Baseline Resolver → Deterministic Scenario Engine → Scenario Result |
| WF-10 Investment Report | API/Job → Reporting Service → Analytics/Research/Scenario/Decision Context → Versioned Report |
| WF-11 AI Analyst | API → AI Orchestration → Authorization → Tool Gateway → Domain Services → Evidence → AI Model Adapter → Response/Trace |
| WF-12 Human Decision | API → Authorization → Decision Service → Decision Context → PostgreSQL → Audit |

## 33. IA-0 implementation sequence

After architecture approval, implementation should proceed in controlled increments.

### IA-0A — Repository and application skeleton

Establish:

- backend package boundaries;
- frontend boundary;
- configuration;
- dependency management;
- test structure;
- basic CI;
- API bootstrap;
- health/readiness endpoint;
- database connectivity boundary without domain schema proliferation.

### IA-0B — Security and identity boundary

Establish:

- authentication integration point;
- authorization abstractions;
- user/resource context;
- secrets/configuration handling;
- security testing foundations.

### IA-0C — Persistence foundation

Establish:

- database migration mechanism;
- repository patterns;
- transaction boundary;
- persistence testing;
- audit/provenance persistence foundations.

### IA-0D — Reference and data-ingestion foundation

Establish:

- provider adapter contract;
- raw/validated/canonical separation;
- identifier resolution boundary;
- data-quality status handling;
- ingestion job abstraction.

### IA-0E — Analytics foundation

Establish:

- analytical request/result contracts;
- calculation provenance;
- deterministic calculation execution boundary;
- test harness for financial calculations.

### IA-0F — Governance and observability foundation

Establish:

- audit mechanism;
- structured operational telemetry;
- correlation IDs;
- material action logging;
- configuration/version capture.

AI orchestration should not be implemented as the first functional domain. The governed tool architecture should be established after deterministic domain services exist.

## 34. Architecture decision records

The following decisions should receive ADRs when they become material implementation commitments:

- modular monolith and service-boundary strategy;
- PostgreSQL persistence strategy;
- authentication/authorization approach;
- provider selection and adapter policy;
- canonical security master strategy;
- market/fundamental data retention;
- performance methodology;
- risk methodology;
- event publication strategy;
- background job platform;
- object storage;
- Power BI integration method;
- AI model/provider strategy;
- AI retention/privacy;
- deployment platform;
- scaling/service extraction criteria.

ADRs should record:

- context;
- decision;
- alternatives;
- consequences;
- status;
- date/version.

## 35. Deferred architectural decisions

The following remain intentionally unresolved:

1. Exact Python package names and class structure.
2. Final PostgreSQL schema.
3. ORM choice.
4. Migration tooling.
5. API endpoint/resource naming.
6. Authentication provider.
7. Authorization model and role taxonomy.
8. Security master implementation.
9. Specific market-data providers.
10. Specific fundamental-data providers.
11. Raw-data storage technology and retention.
12. Queue/worker technology.
13. Cache technology.
14. Object storage technology.
15. Performance methodology implementation details.
16. Attribution methodology implementation details.
17. Risk methodology implementation details.
18. Exact monitoring rule language.
19. Power BI semantic model.
20. AI model/provider selection.
21. AI prompt/system-instruction architecture.
22. AI trace retention.
23. Deployment platform.
24. Service extraction criteria.
25. Distributed event infrastructure.

These decisions must be resolved when required by implementation, using ADRs where they materially affect architecture.

## 36. Architecture acceptance criteria

This architecture is considered complete for the IA-0 design stage when:

- domain/application/infrastructure boundaries are explicit;
- logical service boundaries are explicit without requiring microservices;
- dependency direction is defined;
- API responsibilities are separated from domain logic;
- persistence is isolated behind infrastructure;
- external providers are isolated behind adapters;
- canonical data flow is defined;
- temporal integrity is addressed;
- deterministic analytics are authoritative;
- long-running work has an asynchronous execution path;
- AI is constrained to governed tool access;
- authorization inheritance through AI is explicit;
- provenance and audit are first-class;
- frontend and Power BI boundaries are explicit;
- testing layers are defined;
- observability and configuration concerns are addressed;
- implementation sequencing is defined;
- deferred decisions are explicit.

## 37. Architectural conclusion

The approved direction is a **governed modular monolith with explicit domain/application/infrastructure boundaries and logical service interfaces**, backed initially by PostgreSQL, exposed through a FastAPI application interface, with React + TypeScript as the primary web client and Power BI behind a governed reporting boundary.

The architecture deliberately establishes deterministic analytical authority before AI intelligence.

The next implementation artifact is therefore the **IA-0 application/project skeleton**, not a full business-domain implementation.

The skeleton must be derived from this architecture and should establish boundaries without prematurely implementing unresolved domain semantics.
