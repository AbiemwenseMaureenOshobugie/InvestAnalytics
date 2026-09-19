# InvestAnalytics User & System Workflow Specification

**Version:** 0.1  
**Status:** Architectural input  
**Product:** InvestAnalytics  
**Scope:** Initial equity platform — Nigerian and global markets

## 1. Purpose

This specification defines how users and system services interact across the core InvestAnalytics product workflows.

It is the next architectural input after the Product Charter and Project Constitution. The domain model must be derived from these workflows rather than designed independently from assumed entities.

The specification defines:

- user goals and triggers;
- preconditions and required inputs;
- system responsibilities;
- workflow steps;
- outputs and state changes;
- validation and failure behavior;
- evidence and provenance requirements;
- human decision boundaries;
- audit requirements;
- dependencies between workflows.

It does **not** yet define the final database schema, Python package structure, API resource model, or implementation technology details beyond constraints inherited from the foundation documents.

## 2. Authority and relationship to other specifications

This document is subordinate to:

1. the user's final product authority;
2. the Project Constitution;
3. the Product Charter.

For implementation:

**Product Charter + Constitution → Workflow Specification → Domain Model → System Architecture → Implementation**

If a later workflow requirement conflicts with an approved foundational decision, the conflict must be surfaced and resolved explicitly. It must not be silently encoded into the domain model.

## 3. Product operating model

The core product loop is:

**Observe → Analyze → Explain → Investigate → Simulate → Decide → Monitor → Observe**

The workflows in this specification are connected stages of that loop.

The platform is decision-support software. A workflow may prepare evidence, calculations, scenarios, recommendations for investigation, or decision records, but the system must not silently convert those outputs into autonomous investment decisions or trades.

## 4. Actors

### 4.1 Investor

A person who owns, manages, researches, or monitors investments through the platform.

The investor may be an individual user or a member of a professional investment team.

### 4.2 Professional investment user

A user operating within an organizational investment workflow.

The initial workflow model must support professional controls without creating a separate analytical system for individual investors.

### 4.3 Analyst / research user

A user responsible for researching securities, maintaining investment theses, evaluating evidence, and monitoring thesis conditions.

### 4.4 Reviewer / decision authority

A user authorized to review research, analysis, scenarios, or proposed decisions and record a human investment decision.

The precise role hierarchy and permission matrix are deferred to the security/domain architecture derived from these workflows.

### 4.5 System services

The platform itself performs governed functions such as:

- portfolio state management;
- market/fundamental data ingestion;
- validation and normalization;
- deterministic analytics;
- research and evidence management;
- scenario computation;
- monitoring and change detection;
- report generation;
- AI orchestration;
- audit and provenance recording.

### 4.6 External data providers

External providers supply market, fundamental, corporate-action, reference, or other permitted investment data.

Provider-specific behavior must remain behind provider adapters.

### 4.7 AI analyst

The AI layer is an interface and orchestration capability over governed domain services.

It may:

- interpret natural-language requests;
- identify relevant tools;
- retrieve governed evidence;
- invoke deterministic calculations;
- synthesize results;
- explain findings;
- identify missing evidence or uncertainty.

It may not:

- invent authoritative data;
- replace deterministic financial calculations;
- bypass permissions;
- silently alter portfolio state;
- make or execute an investment decision on behalf of the user.

## 5. Cross-workflow principles

Every workflow should satisfy the following where applicable.

### 5.1 Deterministic authority

If a result can be calculated reliably by a deterministic service, that service is authoritative.

Examples include:

- portfolio value;
- return calculations;
- contribution;
- attribution;
- volatility;
- drawdown;
- concentration;
- scenario arithmetic.

AI may explain those results but must not become the source of truth for them.

### 5.2 Evidence and provenance

Material outputs should identify, where applicable:

- source data;
- observation/as-of time;
- calculation or analytical method;
- relevant version;
- research source;
- assumption;
- scenario input;
- user-provided information;
- generated interpretation.

The system must distinguish facts from interpretations.

### 5.3 Reproducibility

A material analytical result should be reproducible from the relevant inputs, definitions, versions, and calculation logic to the extent practical.

### 5.4 Human decision authority

A workflow may inform a decision, but recording a decision is a distinct human action.

The system must not infer that a user accepted an analytical conclusion merely because they viewed it, generated a report, ran a scenario, or asked the AI analyst a question.

### 5.5 Temporal integrity

Financial information is time-sensitive.

The system should preserve relevant:

- effective dates;
- observation dates;
- publication dates;
- transaction timestamps;
- as-of timestamps;
- ingestion timestamps.

The system must not silently treat later-known information as if it had been available at an earlier decision time.

### 5.6 Validation before analysis

Data required for authoritative analysis must pass applicable validation and quality checks before it is used.

Unavailable, stale, conflicting, or invalid data should be surfaced rather than silently filled with fabricated values.

### 5.7 Auditability

Material state changes, analytical executions, research changes, AI tool use, and human decisions should produce traceable records appropriate to the action.

## 6. Workflow inventory

| ID | Workflow | Primary outcome |
|---|---|---|
| WF-01 | Create Portfolio | A governed portfolio context exists |
| WF-02 | Add / Import Holdings | Portfolio holdings are represented from validated inputs |
| WF-03 | Ingest Market Data | Canonical market data is available with provenance and quality status |
| WF-04 | Analyze Portfolio Performance | Reproducible performance and attribution results are produced |
| WF-05 | Investigate a Performance Change | Material performance movement is decomposed and investigated |
| WF-06 | Research a Security | A structured research record is created or updated |
| WF-07 | Create an Investment Thesis | A thesis is recorded with assumptions, evidence, and invalidation conditions |
| WF-08 | Monitor a Thesis | Thesis-relevant changes are detected and presented for investigation |
| WF-09 | Run a Scenario | User-defined scenario outcomes are calculated and explained |
| WF-10 | Produce an Investment Report | A traceable analytical/research report is generated |
| WF-11 | Ask the AI Analyst a Question | AI answers using governed tools and evidence |
| WF-12 | Record a Human Investment Decision | A human decision is explicitly recorded with supporting context |

---

# 7. WF-01 — Create Portfolio

## Objective

Establish a portfolio context in which holdings, transactions, analytics, benchmarks, research relationships, and decisions can be associated.

## Trigger

A user chooses to create a new portfolio.

## Preconditions

- The user is authenticated.
- The user has permission to create a portfolio in the relevant personal or organizational context.

## Inputs

At minimum, the workflow may require:

- portfolio name;
- owner/context;
- base currency;
- investment objective or mandate where applicable;
- benchmark where applicable;
- optional description;
- optional reporting/measurement preferences.

The system should not require fields that are not necessary for the selected portfolio type.

## Main flow

1. User starts portfolio creation.
2. System presents required and optional portfolio configuration.
3. User supplies the configuration.
4. System validates required fields and permissions.
5. System creates the portfolio in an initial active state.
6. System records creation metadata and provenance.
7. System returns the created portfolio context.
8. User may proceed to add/import holdings or transactions.

## Outputs

- newly created portfolio;
- portfolio configuration;
- creation timestamp;
- owner/access context;
- audit record.

## Validation and failure behavior

- Duplicate or conflicting identifiers must be handled deterministically.
- Invalid currency/configuration must be rejected.
- Unauthorized creation must be rejected.
- Partial creation must not leave an ambiguous portfolio state.

## Architectural implications

The domain model must represent portfolio ownership/context, configuration, lifecycle, and access without yet assuming a particular persistence schema.

---

# 8. WF-02 — Add / Import Holdings

## Objective

Establish portfolio positions from validated user-entered or imported investment information.

## Trigger

A user adds a holding manually or imports holdings/transactions from an external source.

## Preconditions

- Target portfolio exists and is accessible.
- Security identifiers can be resolved or explicitly flagged for resolution.
- Required transaction/position fields are available.

## Supported input modes

### Manual entry

The user supplies information such as:

- security;
- quantity;
- acquisition information;
- transaction date;
- price/cost;
- fees where applicable.

### Import

The user supplies a supported file or connected-source dataset.

Imported data must not be treated as canonical merely because it was successfully uploaded.

## Main flow

1. User selects a portfolio.
2. User selects manual entry or import.
3. System validates input structure.
4. System resolves securities against the canonical security/reference layer.
5. System validates dates, quantities, prices, currencies, and required fields.
6. System identifies warnings, ambiguities, duplicates, or unsupported records.
7. System presents validation results where user correction is required.
8. User confirms valid records for application.
9. System records the accepted position/transaction information.
10. System updates portfolio state.
11. System records source and import/entry provenance.
12. System makes resulting holdings available to downstream analytics.

## Outputs

- updated portfolio holdings/position state;
- validation results;
- rejected or unresolved records where applicable;
- provenance;
- audit record.

## Important rule

A holding is not equivalent to a transaction.

The eventual domain model must preserve enough information to distinguish current portfolio state from the events that produced that state.

## Failure behavior

- Unresolved securities must not silently map to an arbitrary instrument.
- Invalid records should be rejected or quarantined with an explanation.
- Duplicate imports should be detectable where practical.
- Import processing should be repeatable and traceable.

---

# 9. WF-03 — Ingest Market Data

## Objective

Acquire external market/reference data, validate it, normalize it, and make approved observations available to analytical services.

## Trigger

A scheduled ingestion, user-requested refresh, or controlled administrative process.

## Preconditions

- A supported provider is configured.
- Provider credentials/configuration are available to the ingestion service.
- Provider adapter is operational.
- Target instruments/markets are known.

## Main flow

1. Ingestion job identifies required data.
2. Provider adapter requests data.
3. Raw provider response is captured where permitted.
4. System records provider, retrieval time, and relevant source metadata.
5. Raw data passes structural and semantic validation.
6. Valid observations are normalized.
7. Normalized records are mapped to canonical platform concepts.
8. Data-quality checks are executed.
9. Accepted observations become available to analytical services.
10. Rejected or questionable observations are retained with quality status and reason where appropriate.
11. Ingestion metrics and audit information are recorded.

## Data pipeline contract

The conceptual flow is:

**provider → raw data → validation → normalization → canonical data model → analytics**

Provider-specific formats must not leak into downstream analytical logic.

## Quality requirements

The ingestion system should be able to identify applicable issues such as:

- missing values;
- duplicate observations;
- invalid timestamps;
- impossible price relationships;
- unexpected gaps;
- identifier mismatch;
- stale data;
- corporate-action discontinuities;
- provider errors.

The exact rules depend on the data type and must be specified before implementation of each dataset.

## Outputs

- accepted canonical observations;
- rejected/quarantined observations;
- quality status;
- provenance;
- ingestion execution record.

---

# 10. WF-04 — Analyze Portfolio Performance

## Objective

Calculate authoritative portfolio performance over a defined period and explain its drivers.

## Trigger

A user requests performance analysis or another workflow requires it.

## Preconditions

- Portfolio exists.
- Relevant portfolio state is available.
- Required market prices and transaction information are available.
- Required data passes applicable quality checks.

## Inputs

- portfolio;
- analysis period;
- performance methodology;
- benchmark where applicable;
- optional comparison period.

## Main flow

1. User selects portfolio and period.
2. System validates data completeness and methodology.
3. System establishes the portfolio state and relevant cash/transaction events.
4. Deterministic performance engine calculates applicable measures.
5. System calculates contribution/attribution where supported.
6. System compares against benchmark where configured.
7. System identifies material contributors/detractors.
8. System records calculation metadata and data lineage.
9. Results are presented to the user.
10. User may proceed to investigation, research, scenario analysis, reporting, or decision recording.

## Potential outputs

Depending on available data and selected methodology:

- absolute return;
- relative return;
- time-weighted return;
- money-weighted return;
- CAGR for applicable periods;
- contribution;
- attribution;
- benchmark comparison;
- portfolio/value time series;
- contributors and detractors;
- data-quality warnings.

## Important rule

The performance engine is authoritative for its defined calculations.

AI may explain the results but must not alter the calculated values.

---

# 11. WF-05 — Investigate a Performance Change

## Objective

Explain a material portfolio performance movement by decomposing it into identifiable drivers and retrieving relevant evidence.

## Trigger

A user notices a performance change, receives a monitoring event, or asks a question such as:

> Why did my portfolio underperform yesterday?

## Preconditions

- Portfolio performance can be calculated for the relevant period.
- Sufficient portfolio and market data exists.
- Attribution/decomposition methods applicable to the portfolio are available.

## Main flow

1. User selects or is presented with a material performance change.
2. System defines the comparison period and measurement basis.
3. Performance engine calculates the authoritative change.
4. Attribution engine decomposes the change into available drivers.
5. System identifies significant contributors and detractors.
6. System retrieves relevant market/fundamental/research evidence.
7. System distinguishes measured facts from contextual explanations.
8. System presents findings and evidence.
9. User can drill into a security, research record, market event, or scenario.
10. Investigation activity is recorded where appropriate.

## Example investigation chain

**Portfolio movement → security contribution → relevant price/fundamental change → evidence → research/thesis context**

The chain must remain evidence-based. A correlation or temporal coincidence must not automatically be presented as a proven causal explanation.

## Outputs

- quantified performance change;
- attribution/decomposition;
- evidence set;
- data-quality warnings;
- unresolved questions;
- links to relevant research/thesis records.

---

# 12. WF-06 — Research a Security

## Objective

Create a structured, traceable research view of a security.

## Trigger

A user selects a security for research.

## Preconditions

- Security is identified in the canonical reference layer.
- Relevant data sources are available or their absence is explicitly reported.

## Research areas

The workflow may include:

- business profile;
- market/industry context;
- financial fundamentals;
- valuation;
- profitability;
- balance-sheet characteristics;
- cash-flow characteristics;
- competitive position;
- risks;
- catalysts;
- management/governance information where supported;
- market behavior;
- existing research documents;
- analyst notes;
- investment thesis;
- assumptions;
- evidence;
- invalidation conditions.

## Main flow

1. User selects security.
2. System retrieves canonical security identity.
3. System retrieves available market and fundamental information.
4. System retrieves existing research artifacts.
5. User creates or updates structured research.
6. User attaches or references evidence.
7. System records source and timestamps.
8. User may formulate or update a thesis.
9. System preserves research history/version information.
10. User may initiate monitoring or reporting.

## Outputs

- structured research record;
- evidence references;
- assumptions;
- risks/catalysts;
- research version/history;
- optional linked thesis.

## Governance rule

The platform must distinguish:

- externally sourced facts;
- calculated metrics;
- user-authored interpretation;
- AI-generated interpretation;
- assumptions;
- unresolved claims.

---

# 13. WF-07 — Create an Investment Thesis

## Objective

Record the reasoning that supports an investment thesis in a form that can later be tested and monitored.

## Trigger

A user decides that a security or investment warrants an explicit thesis.

## Preconditions

- Security exists.
- User has appropriate research context or can explicitly create a thesis with incomplete evidence.
- User has permission to create/update the thesis.

## Required conceptual components

A thesis should support:

- thesis statement;
- investment rationale;
- assumptions;
- supporting evidence;
- risks;
- catalysts;
- invalidation conditions;
- expected monitoring indicators;
- creation/update timestamps;
- author;
- relevant evidence provenance.

## Main flow

1. User starts thesis creation.
2. System associates the thesis with the relevant security/research context.
3. User records thesis statement.
4. User records key assumptions.
5. User associates supporting evidence.
6. User defines material risks and invalidation conditions.
7. User identifies indicators that should be monitored.
8. System validates required structure.
9. System records thesis version and provenance.
10. Thesis becomes available for monitoring.

## Central research relationship

**Thesis → Assumptions → Evidence → Monitoring**

The system should make this relationship navigable in both directions.

## Important rule

A thesis is a structured human research artifact. AI may assist in drafting, organizing, or challenging it, but authorship and final acceptance remain explicit human actions.

---

# 14. WF-08 — Monitor a Thesis

## Objective

Detect and present material changes that may support, challenge, or invalidate an existing investment thesis.

## Trigger

A scheduled monitoring process, newly ingested evidence, or a user-requested thesis review.

## Preconditions

- Thesis exists.
- Thesis contains monitorable assumptions, evidence, or conditions.
- Relevant data sources are available.

## Main flow

1. System identifies active theses due for monitoring.
2. System evaluates configured indicators and conditions.
3. System detects relevant changes.
4. System evaluates whether changes are material under defined monitoring rules.
5. System associates detected changes with affected assumptions or invalidation conditions where the relationship is explicitly defined.
6. System retrieves supporting evidence.
7. System creates an investigation/monitoring result.
8. User reviews the result.
9. User may update research, revise the thesis, run a scenario, or record a decision.
10. User action and thesis version changes are recorded.

## Monitoring states

The exact state vocabulary is deferred, but the workflow must support at least the distinction between:

- no material change detected;
- material change requiring investigation;
- evidence supporting an assumption;
- evidence challenging an assumption;
- potential invalidation;
- insufficient evidence.

The system must not equate a detected change with an automatic buy/sell instruction.

---

# 15. WF-09 — Run a Scenario

## Objective

Evaluate how portfolio or investment outcomes change under explicit user-defined assumptions.

## Trigger

A user wants to explore a hypothetical condition.

Examples include:

- price change;
- earnings change;
- margin change;
- FX movement;
- interest-rate movement;
- allocation change;
- stress event;
- portfolio rebalancing assumption.

The supported scenario dimensions must be defined by the specific analytical module.

## Preconditions

- Required baseline data exists.
- Scenario variables are supported.
- User has access to the relevant portfolio/investment.

## Main flow

1. User selects portfolio/security and scenario type.
2. System loads the baseline state.
3. User supplies scenario assumptions.
4. System validates assumptions and units.
5. Deterministic scenario engine calculates outputs.
6. System identifies changed assumptions and affected metrics.
7. System presents baseline versus scenario results.
8. System records scenario inputs and calculation metadata.
9. User may compare scenarios, investigate effects, generate a report, or record a decision.

## Outputs

- scenario assumptions;
- baseline metrics;
- scenario metrics;
- absolute/relative changes;
- sensitivity information where supported;
- methodology;
- provenance and reproducibility metadata.

## Important rule

Scenario outputs are conditional results, not forecasts or guarantees.

The interface must clearly distinguish:

**actual observed data** from **hypothetical scenario assumptions**.

---

# 16. WF-10 — Produce an Investment Report

## Objective

Generate a traceable report combining selected portfolio, analytical, research, risk, scenario, and decision information.

## Trigger

A user requests a report.

## Preconditions

- User has access to requested information.
- Required calculations/research artifacts exist or the report explicitly identifies missing components.

## Main flow

1. User selects report scope.
2. User selects date/as-of period.
3. System gathers permitted portfolio, market, performance, risk, research, thesis, scenario, and decision data.
4. Deterministic analytics generate required calculations.
5. System assembles evidence and provenance.
6. Optional AI layer drafts narrative sections from governed evidence.
7. System identifies generated versus source content.
8. User reviews report.
9. User may finalize/export/share according to permissions.
10. Report version and source context are recorded.

## Report requirements

A report should preserve:

- as-of date/time;
- data sources;
- analytical methodology;
- relevant calculation versions;
- research/thesis versions;
- scenario assumptions;
- material warnings;
- author/reviewer where applicable.

## AI narrative rule

AI-generated narrative must remain grounded in the selected evidence and must not introduce unsupported financial facts.

---

# 17. WF-11 — Ask the AI Analyst a Question

## Objective

Allow natural-language interaction with InvestAnalytics while preserving deterministic authority, evidence provenance, permissions, and human decision authority.

## Trigger

A user asks a natural-language question.

Examples:

- "Why did my portfolio underperform yesterday?"
- "What are my largest equity exposures?"
- "Which holdings contributed most to this month's return?"
- "What assumptions support my thesis on this company?"
- "What changed that could challenge the thesis?"
- "Show me what happens if this holding falls 20%."

## Preconditions

- User is authenticated.
- User has access to the referenced portfolio/research context.
- Required domain tools/data are available.

## Canonical request flow

**User question → AI interpretation → tool/service selection → permission check → deterministic retrieval/calculation → evidence collection → AI synthesis → answer with provenance → human follow-up**

## Main flow

1. AI receives the user request.
2. System determines the requested scope and relevant context.
3. AI identifies required governed tools/services.
4. System checks permissions before accessing data.
5. Tools retrieve or calculate authoritative results.
6. System returns evidence and metadata to the AI layer.
7. AI synthesizes an answer.
8. AI distinguishes facts, calculations, interpretation, assumptions, and uncertainty.
9. System presents the answer and relevant evidence.
10. User may ask follow-up questions, open source records, run scenarios, investigate changes, or record a decision.

## Tool-use rules

The AI layer must use tools for authoritative information.

Examples:

- portfolio value → portfolio analytics service;
- return → performance engine;
- risk metric → risk engine;
- security fundamentals → canonical fundamental-data service;
- thesis state → research/thesis service;
- scenario → scenario engine.

The AI layer must not calculate an authoritative financial result from memory when the governed service is available.

## Failure behavior

If required information is missing, stale, inaccessible, or ambiguous, the AI should say so and identify what is missing rather than inventing an answer.

If multiple interpretations are possible, the system should request clarification when necessary rather than silently selecting a materially different interpretation.

## Audit requirements

Material AI interactions should preserve appropriate traceability, including:

- user request;
- relevant context;
- tools invoked;
- tool results/evidence;
- model/version where required;
- generated response;
- material errors or unavailable tools.

Sensitive information must remain subject to access controls and retention policy.

---

# 18. WF-12 — Record a Human Investment Decision

## Objective

Explicitly record a human decision and the information considered at the time.

## Trigger

A user or authorized decision-maker chooses to record an investment decision.

## Preconditions

- User has permission to record decisions in the relevant context.
- Decision subject is identifiable.
- Relevant supporting context can be linked.

## Decision types

The initial vocabulary is intentionally broad enough to avoid coupling the workflow to autonomous trading. It may include actions such as:

- initiate;
- increase;
- reduce;
- maintain;
- exit;
- defer/investigate;
- other explicitly defined decision types.

The exact controlled vocabulary is a domain decision to be derived from workflow requirements.

## Main flow

1. User opens a decision context.
2. System presents relevant portfolio/research/analysis context.
3. User selects or writes the decision.
4. User records rationale where required.
5. User may link thesis, evidence, scenario, report, or analysis.
6. System records decision timestamp and decision-maker.
7. System captures the relevant as-of context and versions where feasible.
8. User confirms the decision record.
9. System stores the decision as a human-authored event.
10. Future monitoring may reference the decision and its supporting thesis/context.

## Important rule

Viewing, generating, or accepting an AI response must never be treated as a human investment decision.

A decision record requires an explicit human action.

## Outputs

- decision record;
- decision-maker;
- timestamp;
- rationale;
- linked evidence/research/analysis;
- relevant portfolio/security context;
- audit trail.

---

# 19. Cross-workflow state and event requirements

The domain model derived from this specification must support the distinction between:

1. **state** — what is currently true or represented;
2. **events/actions** — what happened;
3. **observations** — what external data reported;
4. **calculations** — what the system derived;
5. **research artifacts** — what humans or authorized AI-assisted workflows recorded;
6. **decisions** — explicit human actions.

This distinction is important because a current holding, a purchase transaction, a market price observation, a calculated return, a research thesis, and a human decision have different provenance and temporal semantics.

## 19.1 Material state transitions

Workflows may create or update state, but state changes should be attributable to an initiating action.

Examples:

- portfolio created;
- holding imported;
- transaction accepted;
- market observation accepted;
- research updated;
- thesis created/versioned;
- monitoring result generated;
- scenario executed;
- report finalized;
- decision recorded.

## 19.2 Event traceability

Where an operation materially affects analytical results, the system should be able to trace:

**input/event → resulting state → calculation → output → user interpretation/decision**

---

# 20. Permissions and security requirements

The workflow specification does not define the final role/permission matrix, but it establishes mandatory security boundaries.

At minimum, the architecture must distinguish access to:

- personal portfolios;
- organizational portfolios;
- holdings and transactions;
- research records;
- thesis records;
- reports;
- decision records;
- AI conversations where retained;
- administrative/provider configuration.

Every workflow that reads or changes protected information must enforce authorization at the service boundary.

AI must inherit the user's effective authorization rather than receiving unrestricted system access.

---

# 21. Data quality and provenance requirements

The following provenance dimensions should be supported where relevant:

| Dimension | Purpose |
|---|---|
| Source/provider | Identify origin |
| Retrieval time | Identify when data entered the system |
| Observation/effective time | Identify when information applied |
| Transformation | Explain normalization/processing |
| Calculation method | Reproduce analytical output |
| Version | Identify relevant logic/research/report version |
| Author/actor | Identify human or service action |
| AI model/tool | Trace AI-assisted activity where applicable |
| Assumption | Distinguish hypothetical/user-defined inputs |
| Quality status | Prevent unqualified data from appearing authoritative |

Not every workflow requires every field, but the architecture must not make these distinctions impossible.

---

# 22. Workflow dependencies

The core dependency chain is:

**WF-01 Create Portfolio**  
→ **WF-02 Add / Import Holdings**  
→ portfolio state

**WF-03 Ingest Market Data**  
→ canonical market/reference observations

Portfolio state + market data  
→ **WF-04 Analyze Portfolio Performance**  
→ **WF-05 Investigate Performance Change**

Security + market/fundamental data  
→ **WF-06 Research Security**  
→ **WF-07 Create Investment Thesis**  
→ **WF-08 Monitor Thesis**

Portfolio/research/market state  
→ **WF-09 Run Scenario**

Portfolio analytics + research + risk + scenario + evidence  
→ **WF-10 Produce Investment Report**

Any governed system capability  
→ **WF-11 Ask AI Analyst**

Research/analytics/scenario/report context  
→ **WF-12 Record Human Investment Decision**

Decision + thesis + portfolio state  
→ future monitoring/investigation cycle

This dependency graph is a workflow dependency, not yet a domain class diagram.

---

# 23. Workflow-to-domain derivation rules

The eventual domain model must be derived by identifying durable concepts required by multiple workflows and distinguishing them from transient operations.

For each candidate domain concept, the derivation process should ask:

1. Which workflow requires it?
2. What state must persist?
3. What event/action creates or changes it?
4. What data does it own?
5. What provenance must remain attached?
6. What other workflow consumes it?
7. What invariants must hold?
8. Is it a domain object, observation, calculation, artifact, event, or service concern?
9. What permissions apply?
10. What lifecycle does it have?

A concept should not be added merely because it is common in financial software.

The domain model should preserve the semantics demonstrated by the workflows rather than force workflows into a prematurely selected schema.

---

# 24. Workflow acceptance criteria

The workflow specification is considered sufficiently defined for domain-model derivation when:

- all twelve required workflows have explicit triggers;
- preconditions are identifiable;
- primary inputs and outputs are identifiable;
- system responsibilities are distinguishable from user actions;
- deterministic calculations have clear authority boundaries;
- AI responsibilities and restrictions are explicit;
- human decision authority is explicit;
- failure/validation behavior is defined at the workflow level;
- provenance and audit requirements are represented;
- workflow dependencies are documented;
- state, events, observations, calculations, research artifacts, and decisions are conceptually distinguished;
- unresolved implementation details are deliberately deferred rather than silently assumed.

---

# 25. Deferred decisions

The following are intentionally deferred to subsequent architectural work:

- final domain entity/class names;
- database schema;
- table relationships;
- API resource structure;
- Python package/module structure;
- frontend component structure;
- exact authentication/authorization implementation;
- exact role hierarchy;
- exact market-data providers;
- exact data-provider schemas;
- detailed analytical formulas and methodology specifications;
- exact monitoring thresholds;
- exact scenario library;
- exact AI model/provider;
- model routing;
- AI memory/retention policy;
- report templates;
- deployment topology.

These decisions must be derived from the approved workflows and documented separately when they become architectural commitments.

---

# 26. Next architectural input

After approval of this workflow specification, the next artifact should be:

**InvestAnalytics Domain Model Specification v0.1**

That specification should derive the domain model from the workflows in this document.

The domain-model phase should not begin by selecting database tables. It should first identify:

- core domain concepts;
- value concepts;
- lifecycle/state;
- domain events;
- relationships;
- invariants;
- ownership boundaries;
- provenance requirements;
- service boundaries;
- workflow-to-domain traceability.

Only after the domain model is stable should the project derive the detailed application architecture and implementation skeleton.

## 27. Versioning

This document is versioned as **v0.1** and represents the initial workflow contract.

Material changes to workflow semantics, human decision boundaries, AI authority, data provenance, or workflow dependencies require explicit review and documentation under the project constitution.
