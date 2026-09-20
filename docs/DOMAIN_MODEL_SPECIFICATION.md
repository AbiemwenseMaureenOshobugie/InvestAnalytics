# InvestAnalytics Domain Model Specification

**Version:** 0.1  
**Status:** Architectural input  
**Product:** InvestAnalytics  
**Derived from:** Product Charter v0.1, Project Constitution v0.1, User & System Workflow Specification v0.1

## 1. Purpose

This specification defines the initial conceptual domain model for InvestAnalytics.

It is derived from the approved product foundation and the twelve user/system workflows. It does **not** begin with database tables, ORM classes, API resources, or frontend components.

The purpose is to establish:

- durable domain concepts;
- value concepts;
- ownership and boundaries;
- lifecycle/state;
- domain events;
- relationships;
- invariants;
- provenance requirements;
- analytical result semantics;
- service responsibilities;
- workflow-to-domain traceability.

Implementation structures must be derived from this model rather than allowing persistence or framework concerns to redefine the domain.

## 2. Architectural derivation chain

The approved architectural sequence is:

**Product Charter + Project Constitution**  
→ **User & System Workflow Specification**  
→ **Domain Model Specification**  
→ **System/Application Architecture**  
→ **Implementation**

The workflow specification is the immediate source for this model.

A domain concept is included because one or more workflows require durable semantics, not because it is conventional in investment software.

## 3. Domain boundaries

The initial domain is divided into the following conceptual areas:

1. **Identity & Access Context** — users, organizational contexts, authorization boundaries.
2. **Portfolio Management** — portfolios, accounts/contexts, holdings, transactions, cash, mandates, benchmarks.
3. **Instrument & Market Reference** — securities/instruments, markets, identifiers, currencies, price observations, corporate actions.
4. **Fundamental Data** — financial statements, reported metrics, derived fundamental observations.
5. **Analytics** — performance, attribution, risk, exposure, concentration, scenario results.
6. **Research** — security research, evidence, assumptions, risks, catalysts, theses.
7. **Monitoring & Intelligence** — monitoring rules, observations of change, investigation opportunities.
8. **Reporting** — report definitions, report versions, included analytical/research context.
9. **Decision Records** — explicit human investment decisions and their supporting context.
10. **AI Interaction & Governance** — AI requests, tool executions, evidence context, generated responses, traceability.
11. **Provenance & Audit** — source lineage, actor/action records, calculation/version metadata, quality status.

These are conceptual boundaries. They are not yet Python packages or microservices.

## 4. Core domain concepts

### 4.1 User

Represents an authenticated human actor interacting with the platform.

A User is an identity, not a portfolio owner by implication.

Important properties include:

- stable identity;
- display/profile information;
- lifecycle status;
- authentication linkage;
- authorization context.

Authentication credentials themselves are an infrastructure/security concern and must not be conflated with investment-domain identity.

### 4.2 Organization

Represents a professional investment context containing users and shared resources.

An individual workflow may operate without an Organization, while professional workflows may require one.

Organization membership and permissions determine access but should not redefine analytical semantics.

### 4.3 Portfolio

Represents a governed investment context whose positions, transactions, cash, performance, risk, research relationships, and decisions can be analyzed together.

A Portfolio has:

- identity;
- owner/context;
- base currency;
- lifecycle state;
- objective/mandate where applicable;
- benchmark association where applicable;
- measurement/reporting preferences where applicable.

A Portfolio is not itself a holding and does not replace transaction history.

### 4.4 Security / Instrument

Represents an investable financial instrument known to the canonical reference layer.

It requires stable identity independent of any one external provider.

It may have:

- canonical identifier;
- provider/external identifiers;
- instrument type;
- issuer relationship;
- currency;
- market/listing relationships;
- lifecycle status.

The initial platform focuses on equities, but the model should avoid embedding equity-only assumptions where doing so would prevent later multi-asset expansion.

### 4.5 Market / Listing

Represents the market or trading venue context in which an instrument is listed or observed.

A Security and its Listing are conceptually distinct because one instrument may have multiple market contexts.

### 4.6 Holding / Position

Represents the portfolio's current or as-of ownership state for a security/instrument.

A Position answers questions such as:

- what quantity is currently held?
- in which portfolio?
- as of when?
- at what cost basis where supported?
- in which currency/context?

A Position is state.

It is not the historical event that created that state.

### 4.7 Transaction

Represents a portfolio event that changes holdings, cash, or investment state.

Examples include:

- purchase;
- sale;
- dividend receipt;
- fee;
- cash movement;
- transfer;
- adjustment.

The precise transaction taxonomy is a subsequent domain decision.

A Transaction must preserve event time and sufficient economic information to reproduce resulting state where the supported transaction type permits it.

### 4.8 Cash Position

Represents cash held within a portfolio/account context and denominated in a currency.

Cash must be modeled separately from securities because it participates in portfolio valuation, performance, allocation, and transaction flows differently.

### 4.9 Benchmark

Represents a reference against which portfolio or security performance may be compared.

A Benchmark should identify:

- reference identity;
- relevant instrument/index context;
- currency/methodology where required;
- applicable observation series.

Benchmark comparison is analytical context, not portfolio state.

## 5. Market and fundamental observations

### 5.1 Market Observation

Represents an externally sourced or otherwise authoritative observation about a market instrument at a defined time.

Examples:

- open;
- high;
- low;
- close;
- adjusted close where defined;
- volume;
- other supported market fields.

An observation must preserve temporal semantics and provenance.

### 5.2 Corporate Action

Represents an event that changes the interpretation or economic state of a security or portfolio holding.

Examples may include:

- split;
- dividend;
- merger;
- rights issue;
- delisting.

The initial model should preserve the distinction between a corporate action and a derived adjusted price series.

### 5.3 Fundamental Observation

Represents a reported or calculated fundamental metric associated with a security and an applicable reporting/effective period.

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

The model must distinguish reported facts from derived metrics.

### 5.4 Financial Statement

Represents a structured reporting artifact from which fundamental observations may be derived.

It should preserve:

- issuer/security relationship;
- reporting period;
- publication/availability time where known;
- statement type;
- source;
- relevant version or restatement context.

## 6. Research domain

### 6.1 Research Record

Represents a structured research artifact about a Security.

It may contain:

- business profile;
- industry/market context;
- financial analysis;
- valuation;
- competitive position;
- risks;
- catalysts;
- management/governance observations;
- analyst notes;
- interpretation;
- linked evidence.

Research is a versioned artifact, not merely a collection of mutable fields.

### 6.2 Evidence

Represents a traceable support item for a research statement, thesis, analytical explanation, or report.

Evidence may originate from:

- market/fundamental data;
- external documents;
- research documents;
- user-provided material;
- calculated results;
- other approved sources.

Evidence must preserve source/provenance and temporal context where applicable.

### 6.3 Assumption

Represents an explicit premise used by research, a thesis, or a scenario.

An Assumption must be distinguishable from an observed fact.

### 6.4 Investment Thesis

Represents a structured human research proposition concerning an investment/security.

A Thesis contains or references:

- thesis statement;
- rationale;
- assumptions;
- supporting evidence;
- risks;
- catalysts;
- invalidation conditions;
- monitoring indicators;
- author;
- version/history.

The conceptual relationship is:

**Thesis → Assumptions → Evidence → Monitoring**

A Thesis is a human decision-support artifact, not an autonomous trading instruction.

### 6.5 Thesis Version

A material revision of a thesis must be distinguishable from its prior state.

Versioning should preserve:

- author/actor;
- timestamp;
- changed content;
- relevant evidence;
- assumptions;
- invalidation conditions;
- monitoring definitions.

This supports reconstruction of what the thesis meant at a historical decision time.

### 6.6 Invalidation Condition

Represents an explicitly defined condition under which a thesis may no longer hold.

An invalidation condition is not itself proof that a thesis is invalid.

The monitoring domain detects evidence relevant to the condition; the human user retains decision authority over the thesis.

## 7. Monitoring and intelligence

### 7.1 Monitoring Rule

Represents a defined condition or indicator used to monitor a thesis, portfolio, security, or other governed context.

A rule should identify:

- target;
- indicator/condition;
- evaluation context;
- applicable frequency or trigger;
- materiality logic;
- version.

Exact thresholds and rule languages are deferred.

### 7.2 Monitoring Result

Represents the output of evaluating a monitoring rule against available evidence.

A result may indicate:

- no material change;
- material change requiring investigation;
- supporting evidence;
- challenging evidence;
- potential invalidation;
- insufficient evidence.

A Monitoring Result is an analytical/observational artifact. It is not an investment decision.

### 7.3 Investigation

Represents a structured analytical context created to understand a material change or question.

An Investigation may link:

- trigger;
- portfolio/security;
- performance movement;
- attribution;
- evidence;
- research;
- thesis;
- scenario;
- unresolved questions;
- user actions.

This concept supports the product loop from **Observe → Analyze → Explain → Investigate**.

## 8. Analytical domain

### 8.1 Analytical Request

Represents a request to calculate or retrieve a defined analytical result.

It should identify:

- subject;
- period/as-of context;
- methodology;
- requested measures;
- relevant benchmark;
- requested comparison;
- input context.

### 8.2 Analytical Result

Represents the output of a deterministic analytical computation.

A result must preserve sufficient metadata to establish:

- calculation type;
- inputs or input references;
- as-of period;
- methodology/version;
- execution time;
- data-quality status;
- provenance.

An Analytical Result is not raw data and not an AI-generated interpretation.

### 8.3 Performance Result

A specialized analytical result covering portfolio or investment performance.

Potential measures include:

- absolute return;
- relative return;
- time-weighted return;
- money-weighted return;
- CAGR;
- contribution;
- attribution;
- benchmark comparison.

The exact formulas and methodology belong in a later analytical methodology specification.

### 8.4 Risk Result

Represents deterministic risk analysis.

Potential measures include:

- volatility;
- covariance/correlation;
- beta;
- Sharpe;
- Sortino;
- drawdown;
- VaR;
- Expected Shortfall;
- concentration;
- liquidity;
- factor exposure;
- stress results.

Risk calculations must remain deterministic and versioned.

### 8.5 Exposure

Represents portfolio sensitivity or allocation to a defined dimension.

Possible dimensions include:

- security;
- sector;
- geography;
- currency;
- factor;
- asset type;
- issuer.

Exposure is a calculated view, not necessarily a stored primitive.

### 8.6 Attribution

Represents decomposition of portfolio performance into defined drivers.

Attribution must identify the methodology and scope because different attribution methods produce different interpretations.

### 8.7 Scenario

Represents a user-defined hypothetical set of assumptions applied to a baseline context.

A Scenario must distinguish:

- baseline state;
- hypothetical inputs;
- calculation method;
- output;
- execution metadata.

A Scenario is not a forecast.

### 8.8 Scenario Result

Represents deterministic outputs produced from a Scenario.

It must preserve baseline/scenario distinction and reproducibility metadata.

## 9. Reporting domain

### 9.1 Investment Report

Represents a governed compilation of portfolio, analytical, research, scenario, and/or decision information.

A report should preserve:

- scope;
- as-of time;
- included source artifacts;
- analytical versions;
- research/thesis versions;
- scenario assumptions;
- author/reviewer;
- finalization state.

### 9.2 Report Version

A finalized report should be immutable or versioned so that historical reports can be distinguished from later revisions.

AI-generated narrative within a report must remain distinguishable from source facts and deterministic calculations.

## 10. Human decision domain

### 10.1 Investment Decision

Represents an explicit human investment decision recorded in the platform.

A Decision contains:

- decision-maker;
- decision type;
- subject;
- timestamp;
- rationale;
- supporting evidence/context;
- linked portfolio/security;
- relevant thesis;
- relevant analysis/scenario/report;
- decision-time context.

The decision is an event/artifact with durable historical meaning.

### 10.2 Decision Context

Represents the analytical/research context associated with a decision at the time it was made.

It should allow later reconstruction of what information and versions were considered, subject to available data and retention policy.

The system must never infer a Decision merely because a user viewed or generated information.

## 11. AI interaction domain

### 11.1 AI Request

Represents a user request sent to the AI analyst.

It may include:

- authenticated user;
- conversation/context;
- natural-language request;
- timestamp;
- relevant selected portfolio/security context.

### 11.2 AI Tool Invocation

Represents an AI-directed request to a governed domain service/tool.

It must preserve:

- tool/service identity;
- input parameters;
- authorization context;
- execution status;
- result reference;
- timestamp;
- relevant version.

### 11.3 AI Response

Represents the generated response returned to the user.

Where retained, it should distinguish:

- generated interpretation;
- cited evidence;
- deterministic tool results;
- uncertainty;
- model/version metadata as required.

An AI Response is not an authoritative financial calculation.

### 11.4 AI Interaction Trace

Represents the trace connecting:

**user request → context → tools → evidence/results → generated response**

Retention, privacy, and exact storage policy are deferred.

## 12. Provenance and governance domain

### 12.1 Source

Represents the origin of information.

A Source may be:

- external market-data provider;
- financial statement/document;
- user input;
- connected data source;
- internal calculated result;
- other approved source.

### 12.2 Data Provenance

Represents lineage metadata associated with an observation or artifact.

Relevant dimensions include:

- source/provider;
- retrieval time;
- observation/effective time;
- transformation;
- quality status;
- external identifier;
- canonical identifier.

### 12.3 Calculation Provenance

Represents lineage for deterministic analytical results.

It should identify:

- calculation type;
- methodology;
- version;
- input references;
- execution timestamp;
- data-quality context.

### 12.4 Artifact Provenance

Represents authorship/version/source lineage for research, thesis, report, scenario, and decision artifacts.

### 12.5 Audit Record

Represents a traceable record of material actions or state changes.

Examples:

- portfolio creation;
- import acceptance;
- research update;
- thesis version creation;
- analytical execution;
- AI tool invocation;
- report finalization;
- decision recording.

Audit records support governance but should not be confused with domain events that carry business meaning.

## 13. Value concepts

The following should be treated conceptually as value objects or immutable value structures where appropriate rather than identity-bearing entities:

### 13.1 Money

Amount + currency.

Arithmetic must not silently mix incompatible currencies.

### 13.2 Quantity

Numeric amount + unit/security context where required.

### 13.3 Price

Numeric value + currency + relevant instrument/time context.

### 13.4 Percentage / Rate

A normalized rate with explicit semantic meaning.

For example, return percentage and fee rate must not become interchangeable merely because both are numeric percentages.

### 13.5 Date Range / Period

Explicit start/end or reporting period semantics.

### 13.6 As-of Context

A temporal boundary describing what information is considered available/relevant for an analysis or decision.

### 13.7 Identifier

A typed identifier with namespace/source semantics.

External provider identifiers must not be assumed to be canonical identifiers.

### 13.8 Data Quality Status

A controlled representation of whether data is accepted, questionable, stale, invalid, incomplete, or otherwise qualified.

The final vocabulary is deferred.

## 14. Lifecycle and state model

The domain must distinguish current state from historical events and versioned artifacts.

### Portfolio lifecycle

Conceptual states:

**Draft → Active → Archived**

Invalid transitions must be rejected.

### Research lifecycle

Conceptual states:

**Draft → Active/Current → Superseded/Archived**

Historical versions remain distinguishable.

### Thesis lifecycle

Conceptual states may include:

**Draft → Active → Under Review / Challenged → Superseded / Closed**

Exact state vocabulary is deferred.

A monitoring result must not directly force a thesis into a terminal state without an explicit domain rule and, where appropriate, human action.

### Report lifecycle

Conceptual states:

**Draft → Reviewed → Finalized → Superseded**

### Decision lifecycle

A recorded Investment Decision should be treated as an immutable historical event/artifact. Corrections should create an auditable correction/revision mechanism rather than silently overwriting history.

### Data observation lifecycle

A raw observation may move through:

**Received → Validated → Accepted / Rejected / Quarantined**

Accepted status is required before an observation becomes authoritative for applicable analytics.

## 15. Core relationships

The principal conceptual relationships are:

**User**
→ owns/participates in → **Portfolio / Organization**

**Portfolio**
→ contains → **Positions**

**Portfolio**
→ records → **Transactions**

**Position**
→ references → **Security**

**Transaction**
→ references → **Security / Cash / Portfolio**

**Security**
→ has → **Listings / Market context**

**Security**
→ has → **Market Observations / Fundamental Observations**

**Financial Statements**
→ produce/support → **Fundamental Observations**

**Security**
→ has → **Research Records**

**Research Record**
→ contains/references → **Evidence / Assumptions**

**Research Record**
→ may contain/link → **Investment Thesis**

**Investment Thesis**
→ references → **Assumptions / Evidence / Invalidation Conditions / Monitoring Rules**

**Monitoring Rule**
→ produces → **Monitoring Result**

**Monitoring Result**
→ may create/support → **Investigation**

**Portfolio**
→ produces → **Performance / Risk / Exposure / Attribution Results**

**Scenario**
→ operates on → **Baseline Portfolio/Security Context**

**Scenario**
→ produces → **Scenario Result**

**Research / Analytics / Scenario**
→ contribute to → **Investment Report**

**User**
→ records → **Investment Decision**

**Investment Decision**
→ references → **Thesis / Evidence / Analytics / Scenario / Report**

**AI Request**
→ invokes → **AI Tool Invocation**

**AI Tool Invocation**
→ obtains → **Domain Result / Evidence**

**AI Tool Invocation + Evidence**
→ supports → **AI Response**

All material concepts
→ require appropriate → **Provenance / Audit**

## 16. Key invariants

### Portfolio and position

1. A Position must belong to a defined portfolio context.
2. A Position must reference a resolvable instrument/security.
3. Position state must have a defined temporal context.
4. A Position must not be used as a substitute for transaction history.

### Transactions

5. A transaction must have an identifiable portfolio/context.
6. A transaction must have an applicable transaction type.
7. Quantities, prices, currencies, and timestamps must satisfy type-specific validation.
8. Accepted transaction records must remain traceable to their source.

### Market data

9. A canonical market observation must have an instrument/context and observation time.
10. Provider-specific identifiers must remain distinguishable from canonical identifiers.
11. Unvalidated data must not silently become authoritative analytical input.

### Analytics

12. A material analytical result must identify its methodology/version.
13. Analytical results must preserve their applicable input/as-of context.
14. AI-generated narrative cannot override deterministic analytical results.

### Research and thesis

15. Evidence must retain provenance sufficient to identify its origin.
16. Assumptions must be distinguishable from observed facts.
17. Thesis revisions must not erase historical meaning.
18. Monitoring results do not constitute human decisions.

### Scenarios

19. Scenario assumptions must be distinguishable from observed baseline data.
20. Scenario results must identify the scenario inputs and methodology.
21. Scenario results must not be represented as guaranteed outcomes.

### Decisions

22. An Investment Decision requires explicit human action.
23. A decision must have an identifiable decision-maker.
24. Decision records must preserve relevant historical context where feasible.
25. AI activity must never be interpreted as implicit human approval.

### Authorization

26. Domain services must enforce access to protected portfolio/research/decision data.
27. AI tool access must inherit effective user authorization.
28. A user must not gain access to another user's or organization's data merely through AI interaction.

## 17. Domain events

The initial conceptual event catalog is:

- PortfolioCreated
- PortfolioArchived
- TransactionRecorded
- PositionStateChanged
- MarketObservationReceived
- MarketObservationAccepted
- MarketObservationRejected
- FundamentalObservationAccepted
- CorporateActionRecorded
- ResearchRecordCreated
- ResearchRecordUpdated
- ThesisCreated
- ThesisVersionCreated
- MonitoringRuleCreated
- MonitoringEvaluationCompleted
- InvestigationCreated
- AnalyticalCalculationCompleted
- ScenarioExecuted
- ReportCreated
- ReportFinalized
- AIRequestReceived
- AIToolInvoked
- AIResponseGenerated
- InvestmentDecisionRecorded

These are domain-level concepts, not yet message-bus event schemas.

Event naming and granularity should be revisited during application architecture design.

## 18. Service boundaries implied by the domain

The domain model suggests the following logical service capabilities:

1. **Portfolio Service** — portfolio configuration, holdings/positions, transactions, cash context.
2. **Reference Data Service** — securities, identifiers, listings, markets, currencies.
3. **Market Data Service** — ingestion, validation, normalization, market observations.
4. **Fundamental Data Service** — financial statements and fundamental observations.
5. **Performance Analytics Service** — performance, contribution, attribution.
6. **Risk Analytics Service** — risk and exposure calculations.
7. **Research Service** — research records, evidence, assumptions.
8. **Thesis Service** — thesis versions, assumptions, invalidation conditions, monitoring definitions.
9. **Monitoring/Intelligence Service** — monitoring evaluation and investigation triggers.
10. **Scenario Service** — scenario definitions and deterministic scenario calculations.
11. **Reporting Service** — report composition, versions, provenance.
12. **Decision Service** — explicit human decision records.
13. **AI Orchestration Service** — AI requests, tool selection, governed tool execution, response synthesis.
14. **Governance/Audit Service** — provenance, audit records, lineage.

These are logical boundaries, not a mandate to deploy separate microservices.

A modular monolith is acceptable at the initial implementation stage if these boundaries remain explicit.

## 19. Workflow-to-domain traceability

| Workflow | Primary domain concepts |
|---|---|
| WF-01 Create Portfolio | User, Organization, Portfolio, Benchmark, Money/Currency, Audit |
| WF-02 Add / Import Holdings | Portfolio, Security, Position, Transaction, Cash Position, Source, Data Quality, Audit |
| WF-03 Ingest Market Data | Provider/Source, Security, Listing, Market Observation, Corporate Action, Data Provenance, Quality |
| WF-04 Analyze Performance | Portfolio, Position, Transaction, Market Observation, Benchmark, Analytical Request, Performance Result, Attribution, Calculation Provenance |
| WF-05 Investigate Performance Change | Performance Result, Attribution, Investigation, Evidence, Research Record, Thesis |
| WF-06 Research Security | Security, Market/Fundamental Observations, Research Record, Evidence, Assumption |
| WF-07 Create Thesis | Security, Research Record, Investment Thesis, Thesis Version, Assumption, Evidence, Invalidation Condition, Monitoring Rule |
| WF-08 Monitor Thesis | Thesis, Monitoring Rule, Monitoring Result, Evidence, Investigation |
| WF-09 Run Scenario | Portfolio/Security, Scenario, Assumption, Analytical Result, Scenario Result |
| WF-10 Investment Report | Portfolio, Analytics, Research, Thesis, Scenario, Evidence, Report, Report Version |
| WF-11 AI Analyst | User, AI Request, AI Tool Invocation, Domain Results, Evidence, AI Response, Audit |
| WF-12 Human Decision | User, Investment Decision, Decision Context, Thesis, Evidence, Analytics, Scenario, Report, Audit |

## 20. What is intentionally not a domain entity

The following should not automatically become persistent domain entities merely because they appear in implementation discussions:

- database table;
- API endpoint;
- ORM model;
- UI component;
- Python class;
- provider-specific response object;
- HTTP request;
- cache entry;
- background job;
- log line;
- AI prompt template.

Some may become infrastructure or application-layer structures.

The domain model represents business meaning, not implementation mechanics.

## 21. Domain versus application versus infrastructure

### Domain layer

Owns:

- investment concepts;
- invariants;
- state transitions;
- business events;
- analytical semantics;
- research/thesis semantics;
- decision semantics.

### Application layer

Coordinates:

- workflow execution;
- authorization checks;
- transaction boundaries;
- domain service invocation;
- use-case orchestration;
- external provider coordination;
- AI tool orchestration.

### Infrastructure layer

Owns:

- PostgreSQL;
- ORM/persistence;
- HTTP;
- provider SDKs;
- file storage;
- queues/schedulers;
- authentication mechanisms;
- model-provider clients;
- deployment concerns.

This separation prevents infrastructure choices from dictating the domain model.

## 22. Persistence implications without schema commitment

The domain model implies that persistence must eventually support:

- stable identities;
- historical events;
- versioned research/thesis/report artifacts;
- temporal observations;
- analytical result metadata;
- provenance;
- audit records;
- relationships between decisions and their supporting context.

It does **not** yet prescribe table names, indexes, normalization level, JSON usage, event storage strategy, or database partitioning.

Those decisions belong to the subsequent system architecture/data architecture phase.

## 23. Open domain decisions

The following require explicit decisions before implementation of their respective modules:

1. Exact portfolio/account distinction.
2. Transaction taxonomy and accounting semantics.
3. Position calculation rules.
4. Corporate-action treatment.
5. Security master/reference-data rules.
6. Market-data canonical schema.
7. Fundamental-data canonical schema.
8. Currency/FX treatment.
9. Performance methodology definitions.
10. Attribution methodology.
11. Risk methodology and parameter conventions.
12. Exposure taxonomy.
13. Research artifact granularity.
14. Evidence type taxonomy.
15. Thesis state vocabulary.
16. Monitoring rule language and materiality rules.
17. Scenario taxonomy.
18. Report templates and finalization semantics.
19. Decision type vocabulary.
20. AI interaction retention policy.
21. Audit retention policy.
22. Organization/role/permission model.
23. Data-quality status vocabulary.
24. Exact provenance granularity.
25. Domain event publication/consumption strategy.

These are not gaps to fill by guessing. Each should be resolved when the corresponding architecture or module requires it.

## 24. Domain model acceptance criteria

This model is ready to serve as the architectural basis for system design when:

- all twelve workflows map to explicit domain concepts;
- current state is distinguished from historical events;
- external observations are distinguished from calculations;
- research artifacts are distinguished from facts;
- assumptions are distinguished from observations;
- scenarios are distinguished from forecasts;
- human decisions are distinct from AI outputs;
- provenance is represented as a first-class requirement;
- versioning is defined for material research/report artifacts;
- authorization boundaries are preserved;
- analytical authority remains deterministic;
- logical service boundaries can be identified without requiring microservices;
- unresolved details are explicitly deferred.

## 25. Next architectural input

The next artifact should be:

**InvestAnalytics System Architecture Specification v0.1**

It should derive from this domain model and define:

- application-layer boundaries;
- module/package boundaries;
- service interfaces;
- persistence strategy;
- API architecture;
- data ingestion architecture;
- analytics execution architecture;
- AI orchestration architecture;
- authorization boundaries;
- provenance/audit architecture;
- testing architecture;
- deployment direction.

Only after that architecture is approved should the project create the Python/API project skeleton and begin implementation of IA-0.
