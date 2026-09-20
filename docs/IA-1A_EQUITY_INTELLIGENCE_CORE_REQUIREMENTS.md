# InvestAnalytics IA-1A Equity Intelligence Core Requirements & Domain Contracts

**Version:** 0.1  
**Status:** Approved implementation-planning specification  
**Product:** InvestAnalytics  
**Milestone:** IA-1 — Equity Intelligence Core  
**Stage:** IA-1A — Requirements & Domain Contracts

## 1. Purpose

IA-1A converts the approved product, workflow, domain, and system architecture specifications into the first implementation-level contract for the Equity Intelligence Core.

This specification defines what the first equity intelligence capability must mean before persistence schemas, provider integrations, or application use cases are implemented.

It is intentionally a contract document, not an implementation specification.

IA-1A establishes:

- the scope of the Equity Intelligence Core;
- the first supported equity concepts;
- required invariants;
- temporal and provenance semantics;
- canonical market/reference-data boundaries;
- fundamental-data semantics;
- portfolio/transaction boundaries required by IA-1;
- validation and quality expectations;
- requirements traceability;
- explicit deferrals for later milestones.

IA-1A does not establish database tables, ORM models, provider-specific schemas, API resources, frontend screens, or production ingestion jobs.

## 2. Authority

IA-1A derives from:

1. Project Constitution;
2. Product Charter;
3. Master Context;
4. User & System Workflow Specification;
5. Domain Model Specification;
6. System Architecture Specification;
7. IA-0A Implementation Skeleton Specification.

The authority chain remains:

**Product requirements → workflows → domain semantics → architecture → implementation**

If implementation reveals a conflict with an approved contract, the conflict must be surfaced rather than silently resolved in code.

## 3. IA-1 objective

IA-1 establishes the first trustworthy equity information foundation on which later portfolio analytics, risk analytics, research, monitoring, reporting, and AI capabilities can depend.

The core objective is:

> Make securities, listings, market observations, corporate actions, fundamental observations, financial statements, portfolios, holdings, and transactions representable as governed canonical concepts with explicit temporal, validation, and provenance semantics.

The milestone is successful only when downstream analytical services can consume validated canonical information without depending on a particular external provider representation.

## 4. Scope

### 4.1 In scope

IA-1 covers the conceptual and implementation contracts for:

1. Security / Instrument reference identity
2. Market / Listing reference identity
3. Security identifiers and provider identifiers
4. Market observations
5. Corporate actions
6. Fundamental observations
7. Financial statements
8. Portfolio identity and configuration required for equity holdings
9. Holdings / positions as portfolio state
10. Transactions as portfolio events
11. Cash position boundary where required to preserve portfolio state semantics
12. Data-source and provenance references required by the above
13. Validation and data-quality status
14. Temporal/as-of semantics
15. Repository/application contracts needed to support these concepts

### 4.2 Not in scope

IA-1A does not define or implement:

- portfolio performance calculations;
- attribution calculations;
- portfolio risk calculations;
- valuation analytics;
- factor analytics;
- investment thesis workflows;
- research authoring;
- monitoring rules;
- scenario engines;
- AI analyst behavior;
- autonomous recommendations or trading;
- production authentication/authorization implementation;
- a specific market-data vendor;
- a specific fundamentals vendor;
- a production database schema;
- frontend portfolio screens;
- Power BI semantic models;
- distributed microservices;
- production-scale job infrastructure.

These remain governed by later milestones unless an explicit architectural decision changes the sequence.

## 5. Equity Intelligence Core boundary

The Equity Intelligence Core is responsible for representing and serving validated investment facts and portfolio state required by later analytical services.

It is not itself an analytics engine.

The boundary is:

**External source → provider/raw boundary → validation → normalization → canonical equity data → application/domain consumers**

For portfolio state:

**User/imported transaction input → validation → canonical transaction → portfolio state**

The core must not allow provider-specific payloads to become the authoritative domain representation.

## 6. Canonical concepts

### 6.1 Security / Instrument

A Security represents the canonical identity of an investable instrument.

Minimum semantic requirements:

- stable canonical identity;
- instrument type;
- issuer relationship where known;
- currency where applicable;
- lifecycle status;
- external/provider identifiers;
- listing relationships.

The canonical identity must not depend on a provider-specific identifier.

The initial implementation focuses on equities but must not introduce unnecessary equity-only assumptions that would make later multi-asset expansion structurally difficult.

### 6.2 Market / Listing

A Market represents a trading venue or market context.

A Listing represents the relationship between a Security and a Market.

The distinction is mandatory because:

- one security may have multiple listings;
- provider identifiers may be listing-specific;
- trading currency may differ by listing;
- market calendars and trading context belong to the listing/market relationship.

A listing must not be treated as a second security merely because a provider supplies a separate symbol.

### 6.3 Identifier

Identifiers must distinguish at least:

- canonical platform identity;
- identifier namespace/type;
- provider-specific identifier;
- applicable security or listing scope.

Identifier resolution must be explicit.

An unresolved external identifier must not silently map to an arbitrary security.

### 6.4 Market Observation

A Market Observation is a time-qualified observation associated with a canonical security/listing context.

The initial contract may support:

- open;
- high;
- low;
- close;
- adjusted close where its definition and source are explicit;
- volume.

Additional fields may be introduced only with an explicit contract.

Each observation must preserve, where applicable:

- security/listing reference;
- observation time/date;
- source/provider;
- retrieval/availability time;
- value fields;
- currency;
- quality status;
- provenance.

Adjusted values must remain distinguishable from raw reported values. An adjusted series must not overwrite the raw observation.

### 6.5 Corporate Action

A Corporate Action represents an event that changes the economic or interpretive context of a security.

Examples:

- dividend;
- split;
- rights issue;
- merger;
- delisting.

A corporate action is an event, not a price adjustment.

Derived adjusted prices remain analytical/data products derived from underlying observations and corporate-action rules.

### 6.6 Fundamental Observation

A Fundamental Observation represents a reported or derived metric associated with a security and a defined reporting/effective context.

Examples include:

- revenue;
- earnings;
- EPS;
- margins;
- assets;
- liabilities;
- cash flow;
- dividends;
- valuation ratios.

The contract must distinguish:

1. reported/source fact;
2. normalized representation;
3. derived metric.

A derived ratio must not be represented as though it were directly reported by the issuer.

### 6.7 Financial Statement

A Financial Statement is a structured reporting artifact from which fundamental observations may be derived.

It must preserve, where available:

- issuer/security relationship;
- statement type;
- reporting period;
- publication/availability time;
- source;
- version/restatement context;
- currency;
- relevant units.

The system must preserve the distinction between reporting period and publication/availability time.

### 6.8 Portfolio

A Portfolio is the governed investment context in which positions, transactions, cash, benchmarks, and later analytics are associated.

IA-1 requires enough portfolio semantics to:

- identify the portfolio;
- establish owner/context;
- define base currency;
- track lifecycle state;
- associate holdings and transactions;
- preserve access context for later security architecture.

Detailed authorization policy remains outside IA-1A.

### 6.9 Holding / Position

A Position represents portfolio state at an as-of point.

It answers questions such as:

- what quantity is held;
- which security/listing is held;
- in which portfolio;
- as of when;
- relevant cost basis where supported.

A Position is state, not an event.

The canonical history must not be reduced to a mutable current quantity if transaction reconstruction is required.

### 6.10 Transaction

A Transaction is an event that changes portfolio investment state.

The initial supported conceptual categories include:

- purchase;
- sale;
- dividend receipt;
- fee;
- cash movement;
- transfer;
- adjustment.

The final taxonomy must be explicit before implementation of transaction persistence.

Transactions must preserve sufficient economic and temporal information to reconstruct supported state changes.

### 6.11 Cash Position

Cash is represented separately from securities.

Cash participates in portfolio valuation and transaction flows differently from securities and therefore must not be encoded as a security holding merely for convenience.

## 7. Temporal contract

Temporal integrity is a first-class requirement.

The system must distinguish, where relevant:

- **observation/effective time** — when the market event or value applies;
- **reporting period** — the financial period covered by a statement;
- **publication/availability time** — when information became available to the platform/user;
- **retrieval/ingestion time** — when the platform obtained the source data;
- **analysis as-of time** — the information boundary for an analysis;
- **transaction time** — when a portfolio event occurred.

### 7.1 As-of rule

When an analysis or later workflow is defined as-of a historical time, the system must not silently include information whose availability time is later than that boundary.

### 7.2 Reporting-period rule

A financial statement's reporting period must not be substituted for its publication/availability time.

### 7.3 Observation rule

A market observation date/time must not be confused with the time at which the platform retrieved it.

## 8. Provenance contract

Every authoritative external observation must be traceable to its source.

Where applicable, provenance must identify:

- source/provider;
- external identifier;
- retrieval/ingestion time;
- source artifact or raw-record reference;
- transformation/normalization context;
- quality status.

Derived values must additionally identify:

- input references;
- calculation/methodology;
- methodology version where material;
- execution context.

Provider provenance is evidence about origin, not a substitute for canonical identity.

## 9. Data-quality contract

Data required for authoritative downstream analysis must pass applicable validation before it becomes analytical input.

At minimum, the contract must support quality states sufficient to distinguish:

- valid/accepted;
- warning;
- rejected;
- quarantined;
- stale/unavailable where applicable.

Quality status must be observable by downstream consumers.

### 9.1 Validation categories

Applicable validation includes:

- structural/schema validation;
- identifier resolution;
- required-field validation;
- timestamp/date validation;
- numeric/range validation;
- currency/unit validation;
- duplicate detection;
- temporal consistency;
- cross-field consistency;
- corporate-action consistency;
- source/provider error handling.

### 9.2 No silent fabrication

Missing or invalid data must not be silently replaced with invented values.

If a required value cannot be established, the system should surface the missing/invalid state.

### 9.3 Quality does not equal truth

A record passing structural validation is not automatically proof that the source is economically correct. Source provenance and domain-level validation remain distinct concerns.

## 10. Canonical normalization contract

Normalization converts provider-specific records into stable InvestAnalytics concepts.

Provider-specific:

- field names;
- symbols;
- payload structures;
- error formats;
- authentication mechanisms;
- rate-limit behavior

must remain behind provider adapters.

Downstream domain/application services consume canonical contracts.

Normalization must preserve the source identity and relevant transformation context.

## 11. Duplicate and idempotency requirements

Repeated ingestion or import of the same source information should not silently create contradictory canonical observations.

The implementation must define stable identity/deduplication keys appropriate to each dataset.

Examples may include combinations of:

- security/listing;
- observation timestamp;
- field/data type;
- source;
- external record identity.

Exact persistence constraints are deferred to IA-1B.

## 12. Identifier-resolution requirements

Identifier resolution is a governed operation.

The system must support:

- known canonical identifier;
- known provider identifier mapped to canonical identity;
- unresolved identifier;
- ambiguous identifier;
- retired/invalid identifier where applicable.

Ambiguity must be surfaced.

A provider symbol must not be assumed globally unique across all markets.

## 13. Market-data contract

The first market-data implementation should be capable of representing at least:

- daily OHLC observations;
- volume;
- raw versus adjusted distinction;
- listing/security context;
- source/provenance;
- quality status;
- observation and availability timestamps.

Intraday data, tick data, order-book data, technical indicators, and derived trading signals are deferred.

The initial contract does not mandate a specific provider.

## 14. Corporate-action contract

Corporate actions must be represented independently of adjusted market observations.

The implementation must preserve:

- action type;
- affected security/listing;
- relevant effective/ex-date semantics where applicable;
- source;
- availability time;
- action terms sufficient for supported downstream transformations.

The system must not silently rewrite historical raw observations because a corporate action was later discovered.

## 15. Fundamental-data contract

The first fundamental-data implementation should support structured reporting facts with explicit:

- metric identity;
- value;
- unit;
- currency;
- reporting period;
- availability/publication time;
- source;
- quality status;
- reported versus derived classification.

Valuation ratios and other derived metrics must identify their methodology and inputs.

The system should support restatement/version context rather than silently replacing historical source facts.

## 16. Portfolio/transaction contract

IA-1 must preserve the distinction:

**Transaction events → portfolio state**

A current position must not become the only record of portfolio history.

For supported transaction types, the system should retain enough information to reconstruct resulting position/cash state, subject to explicit rules for adjustments and imported historical positions.

Manual holdings imports must preserve whether a record originated from:

- direct user entry;
- file import;
- connected source;
- reconstructed transaction history.

Imported data must remain traceable to its origin.

## 17. Application contract

Application services should expose typed use cases rather than provider payloads or ORM objects.

IA-1A requires conceptual support for:

### Reference-data queries

- resolve security;
- resolve listing;
- retrieve security/listing metadata;
- retrieve identifier mappings.

### Market-data queries

- retrieve observations for a security/listing and period;
- retrieve observations subject to an as-of boundary;
- report data-quality/provenance context.

### Fundamental-data queries

- retrieve financial statements;
- retrieve fundamental observations;
- distinguish reported and derived values;
- apply temporal/as-of constraints.

### Portfolio operations

- create portfolio;
- add/validate holdings or transaction inputs;
- retrieve portfolio state;
- retrieve transaction history.

Exact command/query names and API routes are deferred to IA-1B/IA-1C implementation contracts.

## 18. Repository contract

Repositories are infrastructure-facing ports for durable domain data.

They must return canonical domain/application representations rather than:

- provider SDK objects;
- raw HTTP responses;
- ORM entities exposed directly to the domain;
- frontend response models.

Repository interfaces must make important temporal context explicit where retrieval semantics depend on it.

The repository layer must not contain analytical business rules that belong to domain/application services.

## 19. Invariants

The following invariants are mandatory for IA-1 implementation planning:

1. A canonical Security has a provider-independent identity.
2. A Listing is a relationship between a Security and Market context.
3. A provider symbol alone cannot establish global instrument identity.
4. A Position represents state; a Transaction represents an event.
5. Cash is not implicitly a security holding.
6. Raw and adjusted market observations remain distinguishable.
7. Corporate actions are events, not overwritten price observations.
8. Reporting period and publication/availability time remain distinct.
9. Observation/effective time and ingestion time remain distinct.
10. Historical as-of analysis cannot silently use later-available information.
11. External observations retain provenance.
12. Derived values retain their methodology and input lineage where material.
13. Invalid or unresolved identifiers cannot silently enter canonical data.
14. Provider-specific structures cannot leak into canonical domain contracts.
15. Missing required data cannot be silently fabricated.
16. Repeated ingestion should be safely deduplicable/idempotent according to dataset-specific identity rules.
17. A material historical correction must preserve traceability.
18. Downstream deterministic analytics consume validated canonical inputs.

## 20. Requirements traceability

| Requirement | Source |
|---|---|
| Equity-first initial scope | Product Charter §4 |
| Nigerian + global markets | Product Charter §4 |
| Provider abstraction | Constitution §3.6; Architecture §§11.1–11.5 |
| Deterministic authority | Constitution §3.1; Workflow §5.1 |
| Evidence/provenance | Constitution §3.2; Workflow §5.2 |
| Temporal integrity | Workflow §5.5; Architecture §12 |
| Validation before analysis | Workflow §5.6 |
| Security/instrument distinction | Domain Model §4.4 |
| Market/listing distinction | Domain Model §4.5 |
| Position versus transaction | Domain Model §§4.6–4.7 |
| Market observations | Domain Model §5.1 |
| Corporate actions | Domain Model §5.2 |
| Fundamental observations | Domain Model §5.3 |
| Financial statements | Domain Model §5.4 |
| Canonical ingestion pipeline | Workflow §9; Architecture §11 |
| Human decision authority | Constitution §3.3; Workflow §5.4 |
| No autonomous investment action | Constitution §4; Architecture §§15,18 |

## 21. Implementation gates after IA-1A

No implementation should proceed to provider integration or database schema merely because a concept appears in this document.

The next contracts must establish:

### IA-1B — Data Model & Persistence Contracts

Define:

- persistence-oriented aggregates;
- entity/value-object boundaries;
- identifiers;
- relationships;
- repository ports;
- transaction boundaries;
- database constraints;
- migration strategy;
- temporal/provenance storage requirements.

### IA-1C — Market Data Ingestion Foundation

Define:

- provider adapter contract;
- raw record boundary;
- validation rules;
- normalization contract;
- canonical observation contract;
- ingestion execution semantics;
- quality/quarantine handling;
- idempotency behavior.

### IA-1D — Fundamental Data Foundation

Define:

- financial-statement contract;
- fundamental observation contract;
- reported/derived semantics;
- period/availability semantics;
- restatement/version handling;
- source/provenance requirements.

### IA-1E — First Deterministic Equity Analytics

Define the first approved security-level deterministic analytics only after canonical data contracts are stable.

## 22. Explicit non-decisions

IA-1A deliberately does not decide:

- market-data vendor;
- fundamentals vendor;
- database table names;
- ORM;
- API URL structure;
- authentication provider;
- exact transaction taxonomy;
- exact corporate-action taxonomy beyond the conceptual boundary;
- intraday/tick-data support;
- technical-analysis indicators;
- valuation methodology;
- portfolio performance methodology;
- AI model/provider;
- microservice decomposition.

These require later evidence and/or explicit architectural decisions.

## 23. Acceptance criteria

IA-1A is complete when:

- the Equity Intelligence Core boundary is explicit;
- in-scope and out-of-scope behavior is documented;
- Security, Market, Listing, Identifier, Market Observation, Corporate Action, Fundamental Observation, Financial Statement, Portfolio, Position, Transaction, and Cash semantics are explicit;
- temporal semantics are explicit;
- provenance requirements are explicit;
- data-quality states and validation expectations are explicit;
- provider abstraction is preserved;
- position/event distinction is preserved;
- canonical versus raw/adjusted/derived distinctions are explicit;
- core invariants are documented;
- application/repository contract expectations are documented without premature framework coupling;
- IA-1B through IA-1E boundaries are clear;
- no database schema, provider, or analytics implementation is introduced prematurely;
- the specification is committed as a reviewable batch.

## 24. Change-control rule

Any implementation change that materially alters these contracts must identify:

- affected requirement;
- evidence or problem;
- proposed change;
- consequences;
- whether a new ADR or user approval is required.

Do not silently redefine IA-1 contracts in implementation code.
