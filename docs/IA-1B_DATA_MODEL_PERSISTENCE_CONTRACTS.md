# InvestAnalytics IA-1B Data Model & Persistence Contracts

**Version:** 0.1  
**Status:** Implementation-planning specification  
**Product:** InvestAnalytics  
**Milestone:** IA-1 — Equity Intelligence Core  
**Stage:** IA-1B — Data Model & Persistence Contracts

## 1. Purpose

IA-1B translates the approved IA-1A equity intelligence requirements into persistence-oriented contracts without allowing the database, ORM, or provider representation to redefine the domain.

This specification establishes:

- aggregate and entity boundaries;
- value-object expectations;
- identity rules;
- relationships;
- repository ports;
- transaction boundaries;
- persistence constraints;
- temporal and provenance storage requirements;
- migration principles;
- query semantics;
- persistence invariants;
- explicit implementation deferrals.

It does not implement the database, ORM mappings, migrations, provider adapters, API resources, or application workflows.

## 2. Authority

IA-1B is subordinate to:

1. Project Constitution;
2. Product Charter;
3. Master Context;
4. User & System Workflow Specification;
5. Domain Model Specification;
6. System Architecture Specification;
7. IA-0A Implementation Skeleton Specification;
8. IA-1A Equity Intelligence Core Requirements & Domain Contracts.

The derivation chain remains:

**Product requirements → workflows → domain semantics → architecture → persistence contract → implementation**

If a persistence constraint conflicts with a domain invariant, the conflict must be surfaced rather than resolved by weakening the domain model.

## 3. Persistence principles

The persistence design must preserve these principles:

1. Canonical domain identity is provider-independent.
2. Raw source records and canonical records are distinct.
3. Provider-specific identifiers remain mappings, not canonical identity.
4. Position is state; transaction is an event.
5. Financial reporting period and information availability time are distinct.
6. Observation/effective time and ingestion time are distinct.
7. Raw and adjusted market data remain distinguishable.
8. Corporate actions remain independent events.
9. Reported facts and derived metrics remain distinguishable.
10. Provenance is durable, queryable information.
11. Invalid or unresolved data must not silently become authoritative.
12. Historical information must remain reproducible under an as-of boundary.
13. Persistence must support idempotent ingestion.
14. Database structure must not leak into domain contracts.
15. The first implementation remains a modular monolith; no distributed persistence is required.

## 4. Persistence scope

### 4.1 Initial persistence domains

IA-1B establishes persistence contracts for:

- Security / Instrument
- Market
- Listing
- Identifier Mapping
- Market Observation
- Corporate Action
- Fundamental Observation
- Financial Statement
- Data Source
- Provenance / Source Record
- Portfolio
- Position
- Transaction
- Cash Position
- Data Quality / Validation State

### 4.2 Explicitly deferred

The following are not persisted as IA-1B business aggregates:

- performance results;
- risk results;
- attribution;
- factor exposures;
- investment theses;
- research documents;
- monitoring rules/results;
- scenarios;
- reports;
- AI traces;
- investment decisions.

Later milestones may establish their persistence contracts.

## 5. Aggregate boundaries

Persistence aggregates are transaction and consistency boundaries, not merely tables.

### 5.1 Reference aggregate

The reference-data boundary contains:

**Security**
- canonical instrument identity;
- instrument type;
- issuer reference;
- lifecycle status;
- descriptive metadata.

**Listing**
- security reference;
- market reference;
- listing symbol/venue metadata;
- trading currency;
- listing lifecycle.

**Identifier Mapping**
- namespace/type;
- external identifier;
- scope;
- validity;
- source.

Security and Listing must not be merged into a single persistence concept.

### 5.2 Market-observation aggregate

A market-observation record represents a source-qualified observation associated with a Listing.

It must be immutable from the perspective of historical fact.

Corrections are represented through source/version/provenance rules rather than silent mutation of previously used historical observations.

The persistence contract must support:
- observation date/time;
- availability time where supplied;
- OHLC values;
- volume;
- raw/adjusted classification;
- currency;
- source;
- quality state;
- provenance reference.

### 5.3 Corporate-action aggregate

A corporate action is persisted independently of market observations.

It must contain:
- affected security/listing;
- action type;
- effective/ex-date information where applicable;
- terms;
- source;
- availability time;
- quality state;
- provenance.

A corporate action must not be encoded only as an adjustment factor on a price row.

### 5.4 Fundamental-data aggregate

The fundamental-data boundary contains:

**Financial Statement**
- statement identity;
- security/issuer;
- statement type;
- reporting period;
- publication/availability time;
- currency;
- units;
- source;
- version/restatement metadata;
- quality/provenance.

**Fundamental Observation**
- metric identity;
- value;
- unit;
- currency;
- reporting period;
- availability time;
- reported/derived classification;
- methodology reference where derived;
- source/provenance;
- quality.

A derived metric may reference source observations without replacing them.

### 5.5 Portfolio aggregate

A Portfolio is the ownership and configuration boundary.

It includes:
- portfolio identity;
- owner/context reference;
- name/description;
- base currency;
- lifecycle state;
- timestamps.

A portfolio owns or contains positions, transactions, and cash state through explicit relationships.

### 5.6 Transaction aggregate

A Transaction is an immutable portfolio event after acceptance, subject to explicit correction/reversal mechanisms.

It must preserve:
- portfolio;
- transaction type;
- event time;
- settlement time where applicable;
- security/listing where applicable;
- quantity;
- price;
- currency;
- fees/costs;
- cash effect;
- external/import reference;
- source/origin;
- provenance;
- validation state.

The exact transaction taxonomy remains governed by IA-1A and must be finalized before persistence implementation.

### 5.7 Position aggregate

A Position represents portfolio state derived from accepted transaction history and/or an explicitly imported opening state.

The persistence model must not make a mutable current quantity the sole representation of portfolio history.

A position record should be queryable as-of a specified point in time.

Where a material recalculation is required, the source transactions and calculation/version context remain authoritative.

### 5.8 Cash aggregate

Cash is persisted separately from security positions.

The initial model must support:
- portfolio;
- currency;
- balance/state;
- as-of time;
- source or reconstruction context.

Cash movements are represented by transactions/events; cash state is the resulting portfolio state.

## 6. Entity and value-object rules

### 6.1 Entity

An entity has a stable identity independent of mutable descriptive attributes.

Initial entities include:
- Security;
- Market;
- Listing;
- Identifier Mapping;
- Market Observation;
- Corporate Action;
- Financial Statement;
- Fundamental Observation;
- Portfolio;
- Position;
- Transaction;
- Cash Position;
- Data Source.

### 6.2 Value concepts

The implementation should model repeated constrained concepts as value objects where doing so improves correctness and testability.

Expected value concepts include:
- Money;
- Quantity;
- Currency;
- Date/Time range;
- Reporting Period;
- Identifier;
- Instrument/Listing status;
- Data Quality State;
- Provenance Reference;
- Methodology Reference.

Value objects should be immutable and validated at construction.

### 6.3 No primitive leakage

Domain/application contracts should avoid ambiguous primitive combinations when a validated monetary value is required. Money should preserve both amount and currency as one coherent concept.

Exact Python type definitions are deferred to implementation.

## 7. Identity and key contracts

### 7.1 Canonical IDs

Each canonical entity requires a stable internal identifier that is not derived solely from an external provider.

The implementation may use UUIDs or another stable opaque identifier, subject to an ADR if the choice materially affects architecture.

### 7.2 External identifiers

External identifiers require:
- namespace;
- provider/source;
- value;
- scope;
- validity period where applicable.

A ticker/symbol is not globally unique.

### 7.3 Natural uniqueness

The database should enforce appropriate uniqueness constraints for canonical concepts, but natural keys must not replace stable internal IDs.

Examples:
- a Listing cannot have two active identical venue-scoped identities;
- an external identifier mapping cannot be duplicated for the same source/scope/validity;
- an observation identity must prevent duplicate canonical ingestion.

Exact indexes/constraints are implementation details to be finalized with migrations.

## 8. Relationship contracts

Core relationships:

- Security 1→N Listing
- Market 1→N Listing
- Security 1→N Identifier Mapping
- Listing 1→N Identifier Mapping where listing-scoped
- Listing 1→N Market Observation
- Security/Listing 1→N Corporate Action as appropriate
- Security 1→N Financial Statement
- Security 1→N Fundamental Observation
- Portfolio 1→N Transaction
- Portfolio 1→N Position
- Portfolio 1→N Cash Position
- Transaction N→1 Security/Listing when applicable
- Transaction N→1 Source/Data Origin
- Canonical observations N→1 Data Source
- Canonical observations 1→N provenance references where required

Relationships must preserve optionality. A transaction that is purely a cash movement need not reference a security.

## 9. Temporal persistence contract

Temporal fields must be persisted explicitly rather than inferred from database timestamps.

### 9.1 Required temporal concepts

Depending on entity:

- observed/effective time;
- reporting_period_start;
- reporting_period_end;
- published/available time;
- ingested time;
- occurred time;
- settled time;
- valid_from;
- valid_to;
- as_of.

The exact field names may vary during implementation, but their semantics must not.

### 9.2 Time zones

Timestamp fields representing instants must be stored in an unambiguous timezone-aware representation.

Date-only financial periods remain dates rather than timestamps.

### 9.3 Historical reproducibility

An as-of query must be able to exclude information whose availability time is later than the analysis boundary.

The persistence layer must therefore retain availability/publication metadata for information that can affect historical analysis.

## 10. Provenance persistence contract

Provenance must be durable enough to answer:

- Where did this record originate?
- Which external identifier was used?
- When was it retrieved?
- Which raw/source record produced it?
- What normalization/transformation occurred?
- What quality state was assigned?
- Which calculation produced a derived value?

### 10.1 Source

A Data Source identifies a provider or source system.

Minimum concepts:
- source identity;
- source type;
- provider name;
- environment/context where relevant;
- active/inactive status.

### 10.2 Source record

A source/raw record reference identifies the external artifact or ingestion record from which a canonical record was produced.

The initial implementation need not expose raw payloads to the domain.

### 10.3 Transformation reference

A canonical record may retain:
- transformation/normalization version;
- adapter version where material;
- source record reference.

### 10.4 Calculation lineage

Derived observations should retain references to their inputs and methodology when material to reproducibility.

## 11. Data-quality persistence contract

Quality state must be persisted separately from provenance.

Minimum conceptual states:

- accepted
- warning
- rejected
- quarantined
- stale
- unavailable

The implementation may use an enum.

A rejected/quarantined record must not become an input to authoritative analytics without an explicit validation transition.

Quality transitions should be auditable where a record changes state.

## 12. Raw versus canonical persistence

The ingestion architecture requires two distinct conceptual layers:

**Raw/source layer**
- provider payload or source artifact;
- source identity;
- ingestion metadata;
- immutable source reference.

**Canonical layer**
- normalized InvestAnalytics representation;
- domain identity;
- validated values;
- provenance to raw/source record.

The canonical layer must not require downstream consumers to understand provider payload structure.

Raw records are evidence and reconstruction material; canonical records are the governed input to domain/application services.

## 13. Idempotency and deduplication

Ingestion must be safely repeatable.

The persistence layer must provide stable identity/deduplication mechanisms for each dataset.

At minimum, implementation design must distinguish:
- source record identity;
- canonical record identity;
- business identity;
- version/restatement identity where applicable.

A repeated source record must resolve to the same canonical record or an explicitly versioned correction rather than silently creating contradictory facts.

Database uniqueness constraints should enforce the strongest deterministic identity available.

## 14. Restatements and corrections

Historical source information may be corrected or restated.

The persistence model must avoid destructive replacement where doing so would destroy reproducibility.

The implementation must support one of the following explicitly per dataset:

1. immutable versioned records;
2. correction records linked to superseded records;
3. another documented versioning strategy.

A later correction must not erase the evidence that an earlier source version existed.

The exact strategy is a required implementation decision before fundamental-data persistence is finalized.

## 15. Repository ports

Repositories are application/domain-facing contracts implemented by infrastructure.

### 15.1 Reference repositories

Required conceptual operations:

- get security;
- find security by identifier;
- get listing;
- find listing;
- list listings;
- save security;
- save listing;
- save identifier mapping.

Queries must distinguish:
- not found;
- ambiguous;
- invalid/retired identifier.

### 15.2 Market observation repository

Conceptual operations:

- save observations;
- retrieve observations by listing and period;
- retrieve observations subject to availability/as-of boundary;
- detect existing observation identity;
- retrieve provenance/quality context.

### 15.3 Corporate-action repository

Conceptual operations:

- save action;
- retrieve actions by security/listing and effective period;
- retrieve actions as-of availability boundary;
- detect duplicate action identity.

### 15.4 Fundamental repositories

Financial statement operations:
- save statement;
- retrieve statements by security and reporting period;
- retrieve statements as-of availability boundary;
- retrieve version/restatement context.

Fundamental observation operations:
- save observation;
- retrieve by metric/security/period;
- retrieve as-of;
- distinguish reported and derived.

### 15.5 Portfolio repositories

Portfolio operations:
- create/retrieve portfolio;
- save/update permitted portfolio metadata;
- retrieve positions as-of;
- retrieve transaction history;
- retrieve cash state as-of.

Repositories must not calculate portfolio performance or risk.

### 15.6 Transaction repository

Conceptual operations:
- append accepted transaction;
- retrieve transaction by identity;
- retrieve transaction history;
- detect duplicate external/import transaction;
- retrieve transactions in a temporal range.

Transactions should be append-oriented. Corrections use explicit reversal/adjustment/version mechanisms rather than arbitrary mutation.

## 16. Transaction boundaries

Persistence transaction boundaries should align with consistency requirements.

### 16.1 Reference-data write

Creating/updating a canonical Security, Listing, and their identifier mappings must be atomic where the operation establishes a new identity relationship.

### 16.2 Ingestion write

A canonical observation and its required provenance/quality references must become visible atomically.

A partially persisted canonical observation without required provenance is invalid.

### 16.3 Portfolio event

An accepted portfolio transaction and all mandatory event metadata must be committed atomically.

Resulting position/cash state may be materialized or calculated, but the accepted transaction remains the authoritative event.

### 16.4 Derived data

Derived observations should be committed with their methodology/input lineage where required for reproducibility.

## 17. Database constraint requirements

The implementation must enforce, where practical:

- non-null required identity fields;
- valid enum/state values;
- positive/non-negative constraints where domain semantics require them;
- valid reporting-period ranges;
- valid time ordering;
- currency/unit consistency;
- uniqueness/deduplication;
- foreign-key integrity;
- appropriate check constraints;
- no orphan provenance for authoritative canonical records.

Database constraints complement, but do not replace, domain validation.

## 18. Indexing requirements

The first schema should optimize governed access patterns rather than speculative analytics.

Expected query dimensions include:

- security/listing identity;
- provider identifier lookup;
- market observation by listing and date/time;
- availability/as-of filtering;
- corporate actions by security/effective date;
- financial statements by security/reporting period;
- fundamentals by security/metric/period;
- portfolio transactions by portfolio/time;
- positions by portfolio/as-of;
- cash by portfolio/currency/as-of;
- provenance by canonical record.

Exact indexes are deferred to the migration implementation after query contracts are finalized.

## 19. Migration strategy

The initial persistence implementation should use version-controlled database migrations.

Requirements:

- migrations are deterministic and ordered;
- schema changes are reviewed as code;
- destructive migrations require explicit justification;
- migration history is part of repository state;
- test environments can build schema from migrations;
- rollback expectations are documented per migration;
- seed/reference data is separated from schema migration logic.

No manual production schema edits should be required for normal deployment.

## 20. ORM boundary

If an ORM is selected, ORM models belong to infrastructure.

Rules:

- ORM models do not become domain entities by default;
- domain entities are not required to inherit ORM base classes;
- repository adapters translate between persistence models and domain/application representations;
- ORM-specific lazy loading must not leak into domain logic;
- database sessions remain infrastructure concerns.

The specific ORM remains an implementation decision.

## 21. Application-to-persistence dependency direction

The approved direction is:

**Interface/API → Application → Domain**

and:

**Infrastructure → Application/Domain contracts**

For persistence:

**Application use case → Repository Port → Persistence Adapter → PostgreSQL**

Forbidden dependencies include:

- Domain → ORM
- Domain → PostgreSQL driver
- Domain → provider SDK
- Application → provider SDK
- API → ORM query logic
- Analytics → raw provider payloads

## 22. Persistence error contract

Infrastructure errors must be translated at the repository/application boundary.

Conceptual categories include:

- not found;
- duplicate/conflict;
- invalid persistence state;
- unavailable dependency;
- transient database failure;
- integrity violation;
- concurrency conflict.

The domain must not depend on driver-specific exception classes.

Exact exception hierarchy is deferred to implementation.

## 23. Concurrency and consistency

The initial system is a modular monolith and does not require distributed transaction coordination.

Persistence must nevertheless define behavior for:

- duplicate ingestion;
- concurrent portfolio writes;
- conflicting identifier mappings;
- simultaneous updates to mutable reference metadata;
- transaction append conflicts.

Optimistic concurrency/version fields may be introduced where mutable aggregates require them.

Transactions and historical observations should favor append/version semantics over destructive mutation.

## 24. Security and privacy persistence requirements

Even though production authentication is outside IA-1B:

- ownership/context identifiers must be persisted where required;
- sensitive user data must not be mixed into market/reference data unnecessarily;
- secrets/API credentials must never be persisted in ordinary domain tables;
- provider credentials belong to secure configuration/secret infrastructure;
- auditability of privileged persistence operations must remain possible;
- tenant/organization boundaries must be structurally enforceable when multi-user persistence is introduced.

## 25. Data lifecycle

The implementation should distinguish:

- active canonical data;
- superseded historical versions;
- rejected/quarantined source data;
- stale data;
- archived raw artifacts.

Deletion policies must not destroy evidence required for financial reproducibility or audit.

Retention periods are deferred to governance/operations decisions.

## 26. Persistence mapping summary

| Domain concept | Persistence role | Primary identity | Historical concern |
|---|---|---|---|
| Security | Entity | Canonical ID | lifecycle/version metadata |
| Market | Entity | Canonical ID | lifecycle metadata |
| Listing | Entity | Canonical ID | validity/lifecycle |
| Identifier Mapping | Entity/value relationship | Source + scoped identifier | validity interval |
| Market Observation | Immutable record | Dataset-specific observation identity | observation + availability time |
| Corporate Action | Event | Action identity | effective + availability time |
| Financial Statement | Versioned artifact | Statement/version identity | reporting + publication time |
| Fundamental Observation | Fact/derived record | Metric + scope + period/version | availability + methodology |
| Portfolio | Aggregate root | Portfolio ID | lifecycle |
| Transaction | Immutable event | Transaction ID/source identity | occurred/settled time |
| Position | State/materialization | Portfolio + security/listing + as-of | state reconstruction |
| Cash Position | State | Portfolio + currency + as-of | event reconstruction |
| Data Source | Reference entity | Source ID | lifecycle |
| Source Record | Evidence record | Source + external identity | ingestion time |
| Provenance | Evidence relationship | Provenance ID | transformation lineage |
| Data Quality | State | Canonical record + state/version | transitions/audit |

## 27. Required implementation order

After IA-1B, implementation should proceed in this order unless evidence requires a change:

1. persistence configuration and migration tooling;
2. base/shared persistence conventions;
3. Data Source and provenance infrastructure;
4. Security / Market / Listing / Identifier persistence;
5. market observation persistence;
6. corporate-action persistence;
7. financial statement/fundamental persistence;
8. Portfolio / Transaction / Position / Cash persistence;
9. repository adapters and contract tests;
10. integration tests against PostgreSQL.

Provider integration remains IA-1C and must consume the repository/persistence contracts rather than bypass them.

## 28. Required test strategy

Persistence implementation must include:

### Unit tests
- value validation;
- mapping logic;
- identity/deduplication rules;
- temporal constraints.

### Repository integration tests
- create/read/update behavior where permitted;
- uniqueness constraints;
- foreign-key integrity;
- as-of queries;
- provenance linkage;
- quality states;
- transaction atomicity.

### Invariant tests
At minimum:
- provider identity cannot become canonical identity;
- raw and adjusted observations remain distinct;
- later-available data is excluded from historical as-of queries;
- rejected records cannot enter authoritative analytical queries;
- transaction history remains available after position materialization;
- provenance is required for authoritative external observations.

### Migration tests
- fresh database can be built from migrations;
- migrations execute in order;
- schema constraints are active.

## 29. IA-1B acceptance criteria

IA-1B is complete when:

- aggregate boundaries are explicit;
- entity/value-object expectations are explicit;
- canonical and external identity rules are explicit;
- relationships are defined;
- temporal persistence semantics are defined;
- provenance persistence is defined;
- data-quality persistence is defined;
- raw/canonical separation is defined;
- idempotency/deduplication requirements are defined;
- correction/restatement expectations are defined;
- repository ports are defined conceptually;
- transaction boundaries are defined;
- database constraint expectations are defined;
- indexing requirements are defined by governed access patterns;
- migration strategy is defined;
- ORM boundary is explicit;
- dependency direction is preserved;
- persistence error categories are defined;
- security/privacy persistence constraints are documented;
- implementation order and tests are defined;
- no database schema, ORM, provider, or production migration code is introduced prematurely;
- the contract is committed as one coherent reviewable batch.

## 30. Next gate

The next milestone is:

**IA-1C — Market Data Ingestion Foundation**

IA-1C must define the provider adapter, raw record, validation, normalization, canonical observation, ingestion execution, quarantine, and idempotency behavior before a concrete market-data provider is integrated.

A provider must not be selected merely because its SDK is convenient. Provider selection should be evaluated against coverage, provenance, licensing/usage constraints, reliability, identifier quality, corporate-action support, historical depth, and Nigerian/global market requirements.

## 31. Change control

Any implementation change that materially alters this persistence contract must identify:

- affected IA-1A/IA-1B requirement;
- evidence or failure motivating the change;
- proposed contract change;
- migration consequences;
- reproducibility/audit consequences;
- whether an ADR or user approval is required.

Persistence convenience must not silently redefine domain semantics.
