# IA-1C Market Data Ingestion Foundation Specification

**Status:** Draft for review  
**Milestone:** IA-1C — Equity Intelligence Core / Market Data Ingestion Foundation  
**Date:** 2026-09-20  
**Scope:** First external market-data ingestion foundation for Nigerian and global equities

## 1. Purpose

IA-1C is the first implementation milestone that crosses the InvestAnalytics boundary into external market-data providers.

Its purpose is to establish a governed ingestion path from external providers into provider-independent canonical market-data contracts while preserving raw source evidence, provenance, temporal semantics, validation state, and idempotency.

IA-1C is an ingestion foundation, not a complete market-data platform. It must prove the boundaries required for later portfolio analytics, research, monitoring, and AI-assisted analysis without allowing provider APIs to become the system's canonical model.

The target flow is:

```
Provider
  ↓
Provider Adapter
  ↓
Raw Source Record / Artifact
  ↓
Validation
  ↓
Normalization
  ↓
Canonical Domain Contract
  ↓
Persistence
  ↓
Deterministic Analytics / Later Workflows
```

Every accepted canonical observation must remain traceable back through this chain.

## 2. Authority

IA-1C is subordinate to:

1. `docs/PROJECT_CONSTITUTION.md`
2. `docs/PRODUCT_CHARTER.md`
3. `docs/MASTER_CONTEXT.md`
4. `docs/USER_SYSTEM_WORKFLOW_SPECIFICATION.md`
5. `docs/DOMAIN_MODEL_SPECIFICATION.md`
6. `docs/SYSTEM_ARCHITECTURE_SPECIFICATION.md`
7. `docs/IA-0A_IMPLEMENTATION_SKELETON_SPECIFICATION.md`
8. `docs/IA-1A_EQUITY_INTELLIGENCE_CORE_REQUIREMENTS.md`
9. `docs/IA-1B_DATA_MODEL_PERSISTENCE_CONTRACTS.md`
10. Accepted IA-1C ADRs:
   - `ADR-IA-1C-001_PROVIDER_SELECTION.md`
   - `ADR-IA-1C-002_RAW_RECORD_STORAGE.md`
   - `ADR-IA-1C-003_CI_GATING.md`

If implementation pressure conflicts with these contracts, stop and resolve the contract conflict before coding.

## 3. Architectural decisions inherited by IA-1C

### 3.1 First provider pair

The first adapter pair is:

- `ng_primary` — Kobo Terminal, formerly NGX Pulse, for the Nigerian market.
- `global_primary` — EODHD for global market coverage.

These selections are provisional for eventual production/vendor licensing.

Before production use, current API access, rate limits, historical coverage, corporate-action coverage, raw retention rights, display/redistribution rights, pricing, and commercial terms must be verified.

Provider marketing names are infrastructure metadata, not domain identifiers.

### 3.2 Raw-record storage

IA-1C uses a hybrid raw-storage boundary:

- PostgreSQL stores source-artifact metadata and provenance metadata.
- Object storage stores immutable raw payloads/artifacts.

Application/domain contracts must remain storage-vendor independent.

The application-facing abstraction is conceptually:

```
store(payload, metadata) → source_artifact_reference
retrieve(source_artifact_reference) → payload
```

S3, MinIO, s3mock, LocalStack, or another implementation must not leak into domain contracts.

### 3.3 CI

CI runs on every push to `main`, including documentation-only commits, and on pull requests.

No docs-only `paths-ignore` rule is introduced.

A committed batch is not considered fully closed until the resulting HEAD SHA has a directly verified CI result appropriate to the repository workflow.

## 4. Scope

IA-1C covers:

- provider adapter contracts;
- provider configuration and credential boundaries;
- provider/source identity;
- market/listing identity resolution;
- raw source-record capture;
- immutable raw artifact storage;
- validation;
- normalization;
- canonical market observations;
- corporate-action ingestion boundary;
- ingestion execution;
- batching and pagination;
- idempotency and deduplication;
- retry/error classification;
- quarantine/rejection;
- provenance;
- temporal/as-of semantics;
- data-quality state transitions;
- source-artifact metadata;
- persistence integration;
- provider-neutral tests;
- adapter contract tests;
- local/CI storage testing;
- operational documentation required to run the ingestion foundation.

IA-1C does not cover:

- portfolio performance analytics;
- portfolio valuation;
- risk analytics;
- investment research workflows;
- thesis management;
- monitoring intelligence;
- scenario analytics;
- investment reports;
- AI analyst behavior;
- autonomous investment decisions;
- trading/execution;
- unrestricted provider-specific domain models;
- production redistribution licensing;
- broad multi-asset ingestion;
- full historical backfill of every supported market.

## 5. Design principles

### 5.1 Provider independence

External response schemas are not canonical schemas.

Provider adapters translate external representations into explicit internal contracts.

### 5.2 Evidence before interpretation

Raw source evidence is retained before normalization produces an interpreted canonical representation.

### 5.3 Deterministic transformation

Validation and normalization must be deterministic for the same source record, contract version, and relevant reference data.

### 5.4 Temporal integrity

The system must distinguish:

- event/observation time;
- effective time;
- reporting period;
- information availability time;
- ingestion time.

No ingestion shortcut may silently convert these into one timestamp.

### 5.5 No silent promotion

Unresolved, invalid, ambiguous, or quarantined source data must not silently become authoritative canonical data.

### 5.6 Reproducibility

Historical analysis must be able to identify the source artifacts and transformation/provenance information used to create a canonical observation.

### 5.7 Human decision authority

IA-1C produces data and evidence for downstream deterministic analytics. It does not make investment decisions.

## 6. Provider adapter boundary

The provider adapter is an infrastructure component implementing an application-facing contract.

Conceptual boundary:

```
Application
    │
    ▼
MarketDataProviderPort
    │
    ├── ng_primary adapter
    │       └── Kobo Terminal client
    │
    └── global_primary adapter
            └── EODHD client
```

The domain layer must not import:

- provider SDKs;
- HTTP client implementations;
- provider-specific response classes;
- provider credential objects;
- provider endpoint names.

The application layer may depend on provider-neutral ports and DTO/contracts required to orchestrate ingestion.

Infrastructure owns provider-specific translation.

## 7. Stable provider identifiers

IA-1C defines these internal adapter identifiers:

| Internal ID | Market scope | External provider |
|---|---|---|
| `ng_primary` | Nigerian equities | Kobo Terminal |
| `global_primary` | Global equities | EODHD |

The mapping is configuration/infrastructure metadata.

Business logic must never branch on provider marketing strings.

A provider replacement must preserve canonical contracts wherever possible and be handled as an infrastructure change plus an ADR when architecture changes.

## 8. Provider credential boundary

Provider credentials are infrastructure secrets.

Requirements:

- credentials must not be stored in domain tables;
- credentials must not be committed to Git;
- credentials must not appear in raw-record payloads unless the provider itself returns them, in which case the ingestion layer must prevent accidental persistence of secrets;
- credentials must not be exposed to domain services;
- logs must redact authorization headers, API keys, tokens, and equivalent secrets;
- provider authentication failures must be represented as operational/provider errors, not domain validation failures.

Configuration should identify the adapter and non-secret operational settings. Secret values come from environment/secret management mechanisms.

## 9. Provider capability contract

Each adapter must expose or declare capabilities without leaking provider-specific API shape.

Capabilities should be explicit enough for scheduling and validation, including:

- supported markets/listings;
- supported observation frequencies;
- historical retrieval support;
- corporate-action support;
- identifier/reference-data support;
- pagination/batching support;
- maximum request scope where applicable;
- rate-limit information when known;
- adjustment semantics;
- active/delisted coverage where applicable.

Capabilities are metadata about an adapter. They must not alter canonical entity definitions.

## 10. Provider-neutral retrieval contract

The application-facing provider port should conceptually support:

```
get_security_reference(request)
get_listing_reference(request)
get_market_observations(request)
get_corporate_actions(request)
```

The exact Python protocol/class names are an implementation decision subject to IA-1C coding conventions.

Requests must express business needs, not provider endpoints.

For example, the application should request a market-observation range for a canonical listing/provider mapping, rather than request an endpoint path such as `/eod/AAPL.US`.

Responses should contain provider-neutral source records sufficient for:

- raw retention;
- validation;
- normalization;
- provenance;
- canonical mapping.

## 11. Source record contract

A source record represents data received from an external provider before canonical interpretation.

Minimum conceptual fields:

- adapter ID;
- provider/source identity;
- source record identity, where available;
- request/execution identity;
- retrieval timestamp;
- source payload reference;
- payload hash;
- media/content type;
- source event/observation timestamps as supplied;
- raw provider identifiers;
- ingestion status;
- validation status;
- provenance reference.

A source record is not itself a canonical market observation.

## 12. Source artifact contract

A source artifact is the immutable stored representation of raw provider payload.

Minimum metadata:

- unique artifact reference;
- adapter/provider identity;
- retrieval timestamp;
- request/execution identity;
- provider/source record identity where available;
- content hash;
- content/media type;
- byte/object size where available;
- object-storage reference;
- ingestion status;
- validation status;
- retention/lifecycle metadata;
- provenance linkage.

The raw artifact must be immutable.

A corrected provider response creates a new artifact rather than mutating the historical raw artifact.

## 13. Object-key strategy

The exact object-storage technology is intentionally abstracted.

Object keys should be deterministic enough to support operational lookup while avoiding dependence on provider endpoint naming.

A recommended logical pattern is:

```
<environment>/<adapter>/<data-type>/<retrieval-date>/<artifact-id>
```

The artifact ID remains the stable reference.

Provider symbols may appear as metadata but should not be required as the sole object identity because symbols can be reused, renamed, or delisted.

The final implementation must document whether content-addressed hashing, UUIDs, or a hybrid is used.

## 14. Content hashing

Every stored raw artifact must have a cryptographic content hash.

The hash is used for:

- duplicate detection;
- immutable-content verification;
- idempotency support;
- provenance;
- corruption detection.

Hash equality indicates identical stored content. It does not by itself prove that two records are semantically equivalent.

The hashing algorithm must be explicit in implementation documentation.

## 15. Identifier resolution

Provider identifiers must be mapped to canonical Security/Listing concepts through explicit resolution.

Conceptual flow:

```
provider identifier
       ↓
provider mapping
       ↓
candidate canonical identity
       ↓
validation/conflict checks
       ↓
resolved / unresolved / quarantined
```

Resolution must consider, where available:

- provider symbol;
- exchange/market;
- listing;
- security identifier;
- provider instrument ID;
- ISIN or equivalent;
- effective validity period;
- active/delisted status.

No ambiguous provider identifier may be silently mapped to a canonical listing.

## 16. Identifier mapping states

A mapping should have an explicit state such as:

- `resolved`;
- `unresolved`;
- `ambiguous`;
- `rejected`;
- `superseded`.

The exact enum/type is implementation-defined but must preserve the semantic distinction.

An unresolved mapping may be retained as source evidence and operational work but must not be treated as an authoritative canonical observation.

## 17. Market-observation normalization

Provider observations must be normalized into the IA-1A/IA-1B canonical market-observation contract.

Normalization must explicitly address:

- timestamp;
- timezone;
- trading session;
- open;
- high;
- low;
- close;
- volume;
- currency;
- listing identity;
- frequency;
- adjusted/unadjusted status;
- source observation identity;
- provenance.

The canonical contract must not inherit provider field names.

## 18. Price integrity rules

At minimum, validation should check:

- required fields are present;
- numeric fields are parseable;
- price values are finite;
- high is not below low;
- high is not below open/close when those fields are present;
- low is not above open/close when those fields are present;
- volume is non-negative when supplied;
- currency is known or explicitly unresolved;
- observation belongs to a resolvable listing;
- timestamps satisfy the expected temporal contract.

A failed check does not necessarily mean the raw record is discarded. The result must be classified into accepted, rejected, or quarantined states according to severity.

## 19. Adjustment semantics

Adjusted and unadjusted observations must never be silently conflated.

IA-1C must preserve:

- whether an observation is raw/unadjusted;
- whether an adjustment was applied;
- adjustment basis/source;
- relevant corporate-action relationship when known.

Provider-specific adjustment flags must be translated into canonical semantics.

If adjustment semantics cannot be determined reliably, the record must remain explicitly unresolved rather than being presented as an authoritative adjusted series.

## 20. Corporate actions

IA-1C establishes the ingestion boundary for corporate actions, including at minimum where supported:

- dividends;
- splits.

The contract must preserve:

- security/listing relationship;
- action type;
- announcement/effective/ex dates where supplied;
- quantities/rates/amounts where applicable;
- currency where applicable;
- provider/source identity;
- provenance;
- correction/version state.

Corporate actions are events and must not be embedded only as fields on market observations.

The relationship between a corporate action and adjusted historical observations must remain queryable.

## 21. Historical and delisted securities

The ingestion foundation must not assume that the current active universe is the complete historical universe.

Where a provider exposes delisted securities, their source/reference records should be retainable.

A listing's active status is temporal.

Historical retrieval must preserve enough identity and temporal metadata to distinguish:

- currently active listing;
- historically active listing;
- delisted listing;
- unresolved listing state.

## 22. Temporal and as-of semantics

IA-1C must preserve at least:

1. observation/event time;
2. effective time where applicable;
3. information availability time where known;
4. ingestion time.

For a source record:

```
observed_at
effective_at
available_at
ingested_at
```

are conceptually distinct.

For historical analysis, the system must not use information that was unavailable at the requested as-of time.

Provider retrieval time is not automatically equivalent to information availability time.

If availability time is not supplied or inferable under an approved rule, the limitation must be recorded.

## 23. Ingestion execution

An ingestion execution represents one controlled attempt to retrieve and process source data.

Minimum conceptual metadata:

- execution ID;
- adapter ID;
- request scope;
- start time;
- end time;
- execution status;
- request count;
- source-record count;
- accepted count;
- quarantined count;
- rejected count;
- error count;
- retry count.

Execution identity must support operational audit and replay.

## 24. Request identity

Each external request should have a traceable request identity.

Where practical, retain:

- adapter ID;
- logical request scope;
- execution ID;
- request timestamp;
- provider request/reference ID if supplied;
- pagination/batch position;
- response status;
- response hash/artifact reference.

Request identity is operational/provenance metadata and is not a domain business key.

## 25. Batching and pagination

Adapters must isolate provider pagination and batching behavior.

The application should request a logical data scope.

The adapter handles:

- page tokens;
- offsets;
- provider-specific batch limits;
- request partitioning;
- continuation;
- provider-specific throttling.

Partial completion must be visible.

A multi-page ingestion is not considered complete merely because at least one page succeeded.

## 26. Rate limiting

Provider rate limits must be enforced at the adapter/infrastructure boundary.

The ingestion scheduler/application may receive provider-neutral retry/throttling signals.

The domain layer must not contain provider-specific sleep intervals or quota logic.

Rate-limit parameters must be configurable without code changes where practical.

Actual limits must be verified from current provider documentation before production configuration.

## 27. Retry classification

Errors should be classified into at least:

### Retryable

Examples:

- transient network failure;
- timeout;
- temporary provider availability failure;
- provider rate-limit response;
- explicitly retryable server response.

### Non-retryable

Examples:

- invalid credentials;
- malformed request;
- unsupported instrument;
- invalid date range;
- revoked access;
- permanent provider rejection.

### Unknown

Unknown errors must fail safely and retain enough context for investigation.

Retries must be bounded.

The system must avoid creating duplicate canonical observations when a request is replayed.

## 28. Idempotency

Repeated ingestion of the same source record must not create duplicate authoritative observations.

Idempotency should use stable source/provider identity where available, supplemented by deterministic identity components and content hashing.

Conceptually:

```
same source identity
+
same logical observation
+
same applicable version
→
same canonical record or explicit no-op
```

A changed source payload with the same provider identity must not overwrite historical evidence. It should be treated as a correction/revision according to the persistence contract.

## 29. Correction and restatement handling

Provider corrections must preserve prior evidence.

The system must distinguish:

- original source artifact;
- corrected source artifact;
- supersession relationship;
- validation state;
- canonical version/effective state.

No destructive overwrite of raw evidence is permitted.

Downstream canonical data may be superseded according to IA-1B correction semantics, but the original source artifact remains auditable.

## 30. Validation pipeline

The processing sequence is:

```
retrieve
  ↓
persist raw artifact
  ↓
parse
  ↓
validate source structure
  ↓
resolve identifiers
  ↓
validate temporal semantics
  ↓
validate field/value invariants
  ↓
normalize
  ↓
validate canonical contract
  ↓
persist canonical result
```

Raw persistence occurs before interpretation so that failed normalization does not destroy source evidence.

## 31. Data-quality states

IA-1C should represent data-quality state transitions explicitly.

Minimum semantic states:

- received;
- validated;
- normalized;
- accepted;
- quarantined;
- rejected;
- superseded.

The exact persistence model may represent these as status fields, state records, or both.

State transitions must be auditable.

## 32. Quarantine

Quarantine is used when raw data is retained but cannot safely become authoritative.

Examples:

- ambiguous identifier mapping;
- unresolved currency;
- inconsistent timestamp semantics;
- provider response shape outside the expected contract;
- suspicious price invariants;
- uncertain adjustment semantics.

Quarantined data remains available for investigation/reprocessing.

Quarantine must not be presented to downstream analytics as authoritative data unless explicitly promoted through a governed process.

## 33. Rejection

Rejection means the source record cannot enter the canonical dataset under the current contract.

The rejection reason must be explicit.

Raw evidence should remain retained when permitted by provider terms.

Examples:

- malformed payload;
- irreparably invalid required fields;
- unsupported data type;
- impossible canonical mapping.

## 34. Provenance

Accepted canonical data must be traceable through:

```
canonical observation
    ↓
normalization result
    ↓
validation result
    ↓
source record
    ↓
raw artifact
    ↓
provider request/execution
    ↓
adapter/provider identity
```

Provenance should also identify relevant transformation/contract versions where needed for reproducibility.

Provenance is queryable metadata, not merely an application log.

## 35. Data lineage and transformation version

The ingestion system should record enough information to answer:

- Which provider produced this observation?
- Which adapter processed it?
- When was it retrieved?
- Which raw artifact produced it?
- Which validation rules were applied?
- Which normalization contract/version was used?
- Was the observation later superseded?
- Which source identifier mapped to the canonical listing?

Transformation/version identifiers should be stable and auditable.

## 36. Persistence boundary

IA-1C consumes the IA-1B repository and persistence contracts.

Conceptual path:

```
Application
   ↓
Repository Port
   ↓
Persistence Adapter
   ↓
PostgreSQL
```

Raw payload path:

```
Application
   ↓
Source Artifact Port
   ↓
Object Storage Adapter
   ↓
Object Storage
```

The domain/application layer must not contain SQL, ORM models, or object-storage SDK calls.

## 37. Transaction boundaries

A single ingestion transaction should not require a distributed transaction spanning PostgreSQL and object storage.

The implementation must define safe sequencing and recovery for:

1. raw artifact write;
2. metadata persistence;
3. validation;
4. canonical persistence.

If object storage succeeds and metadata persistence fails, the artifact must remain recoverable and reconcilable.

If metadata exists without a valid object, the source-artifact state must make the incomplete condition visible.

The exact reconciliation mechanism is an implementation concern but must be tested.

## 38. Object-storage implementation for local development and CI

The application contract remains vendor independent.

For local development, a fuller S3-compatible implementation such as MinIO may be used.

For CI/repository integration tests, the accepted ADR identifies lightweight S3-compatible emulation as the preferred direction, with s3mock as the leading candidate and moto as a Python-native alternative.

The final test implementation must be selected based on:

- deterministic startup;
- test isolation;
- compatibility with required object operations;
- CI execution time;
- maintenance burden.

This is an infrastructure/testing decision, not a domain contract.

## 39. Provider-specific SDK policy

Provider SDKs may be used only inside infrastructure adapters.

Requirements:

- no SDK import in domain;
- no SDK import in application;
- no provider response object in application contracts;
- no provider-specific exception escaping the adapter boundary;
- no provider-specific credential object outside infrastructure.

Direct HTTP clients are acceptable where an SDK adds unnecessary coupling, provided the same isolation rules apply.

## 40. Provider-specific mapping policy

Provider-specific behavior belongs in explicit adapter translation code.

Examples:

- ticker suffix parsing;
- exchange-code translation;
- date/time parsing;
- corporate-action field mapping;
- adjustment flags;
- pagination;
- rate-limit response parsing.

Do not scatter these rules across domain services.

## 41. Licensing and usage controls

Provider selection is not equivalent to production redistribution approval.

Before production use, verify:

- API access rights;
- historical-data rights;
- raw retention rights;
- internal-use rights;
- display rights;
- redistribution rights;
- derivative-data restrictions;
- caching/retention limits;
- attribution requirements;
- commercial terms.

The platform must be capable of identifying source/provider provenance so that licensing constraints can later be enforced operationally.

No implementation assumption may imply that free/developer access permits production redistribution.

## 42. Coverage boundary

IA-1C initially targets equities in:

- Nigeria;
- global markets supported by the selected global provider.

The first implementation should prove a representative set rather than attempt universal coverage.

Coverage tests should include:

- Nigerian listing;
- global listing;
- at least one identifier mapping;
- historical market observations;
- corporate action where available;
- an active security;
- a delisted/historical security where provider access permits.

Specific securities should be selected during implementation planning based on current provider availability and licensing.

## 43. Provider availability verification gate

Before adapter implementation begins, verify current provider documentation and account access for:

### Kobo Terminal

- current API documentation;
- authentication;
- Nigerian equity endpoint coverage;
- historical observations;
- corporate actions/disclosures;
- identifier/reference data;
- rate limits;
- raw retention terms;
- commercial/display rights.

### EODHD

- current API documentation;
- authentication;
- global equity coverage;
- historical observations;
- active/delisted reference data;
- identifier mapping;
- corporate actions;
- rate limits;
- raw retention terms;
- commercial/display rights.

Evidence of verification should be recorded in implementation planning or an updated decision record.

## 44. Application services

IA-1C may introduce application services for controlled ingestion orchestration.

Examples of responsibilities:

- create ingestion execution;
- request provider-neutral data;
- persist source artifacts;
- invoke validation;
- resolve identifiers;
- normalize records;
- persist accepted canonical records;
- persist quarantine/rejection outcomes;
- report execution results.

Application services must orchestrate; they must not contain provider endpoint logic.

## 45. Domain responsibilities

Domain contracts/rules should own provider-independent semantics such as:

- canonical market observation representation;
- temporal validity;
- identifier mapping state;
- market-observation invariants;
- corporate-action semantics;
- data-quality states;
- provenance relationships.

The domain should remain usable without an internet connection or provider SDK.

## 46. Infrastructure responsibilities

Infrastructure owns:

- HTTP/SDK clients;
- provider authentication;
- request throttling;
- provider pagination;
- provider response parsing;
- object-storage adapter;
- PostgreSQL repository implementations;
- provider-specific operational error mapping.

Infrastructure must translate provider errors into provider-neutral application errors.

## 47. API exposure

IA-1C does not require a public ingestion API.

If an internal API is introduced to exercise the ingestion foundation, it must remain a thin interface over application services.

No provider endpoint should be exposed directly through FastAPI.

No API response should leak provider SDK response models.

## 48. Observability

Ingestion must produce structured operational information sufficient to diagnose:

- execution start/end;
- adapter;
- logical scope;
- request count;
- success/failure;
- retries;
- rate limiting;
- source-record counts;
- validation outcomes;
- quarantine/rejection counts;
- artifact references.

Sensitive credentials and provider secrets must never be logged.

Logs are operational evidence; provenance remains durable/queryable data.

## 49. Testing strategy

IA-1C requires multiple test layers.

### 49.1 Unit tests

Cover:

- provider-neutral contracts;
- validation rules;
- normalization;
- identifier mapping;
- timestamp handling;
- adjustment semantics;
- error classification;
- idempotency key construction;
- data-quality state transitions.

### 49.2 Adapter contract tests

Both `ng_primary` and `global_primary` must satisfy the same provider-neutral adapter contract.

The test suite must prove that both adapters can produce compatible canonical representations despite different external schemas.

### 49.3 Repository integration tests

Test:

- source metadata persistence;
- provenance persistence;
- canonical observation persistence;
- uniqueness/idempotency constraints;
- correction/supersession;
- quarantine/rejection;
- temporal queries.

### 49.4 Object-storage integration tests

Test:

- store/retrieve;
- content hash;
- immutable artifact behavior;
- metadata linkage;
- missing artifact detection;
- duplicate artifact handling.

### 49.5 End-to-end ingestion tests

At least one controlled fixture per adapter should exercise:

```
source fixture
→ raw artifact
→ validation
→ identifier resolution
→ normalization
→ canonical persistence
→ provenance query
```

Tests must not depend on live provider availability unless explicitly classified as non-gating external integration tests.

## 50. Fixture policy

CI tests should use deterministic provider fixtures/mocks.

Live provider calls must not be required for ordinary CI success because external outages, quota changes, and credential availability would make repository health nondeterministic.

A separate opt-in integration mode may exercise live providers when credentials and commercial permissions are available.

Live-provider tests must not persist uncontrolled production data into test environments.

## 51. CI requirements

The existing CI pipeline must continue to run on every push and pull request.

IA-1C implementation must preserve:

- backend formatting/linting;
- static/type checks;
- backend tests;
- frontend installation/build/test;
- any newly required database/storage integration tests.

If new service dependencies are added to CI, startup and teardown must be deterministic.

The final IA-1C implementation batch must have a directly verified successful CI run on its exact HEAD SHA.

## 52. Failure isolation

A failure in one provider must not corrupt another provider's ingestion state.

Provider executions are independently identifiable.

A Kobo failure must not invalidate EODHD source artifacts, and vice versa.

A provider outage must not alter previously accepted canonical observations.

## 53. Security requirements

IA-1C must enforce:

- secret exclusion from source control;
- secret redaction in logs;
- least-privilege provider credentials;
- separate development/test credentials where applicable;
- no credentials in raw source artifacts unless unavoidable and sanitized;
- access control around raw artifacts and source metadata;
- auditability of ingestion operations.

## 54. Data lifecycle

IA-1C must distinguish:

1. source acquisition;
2. raw retention;
3. validation;
4. normalization;
5. canonical acceptance;
6. supersession/correction;
7. retention/expiry.

Raw retention policy must respect provider licensing.

Deletion/expiry must not silently destroy required provenance if retention obligations require otherwise.

## 55. Operational reconciliation

A reconciliation process must be possible for incomplete states such as:

- raw artifact exists but metadata is missing;
- metadata exists but object is unavailable;
- source record is accepted but canonical persistence failed;
- canonical record exists without complete provenance;
- provider replay returns a changed payload.

IA-1C need not implement a full operations console, but the persistence state must make these cases detectable.

## 56. Required implementation sequence

Implementation should proceed in coherent batches:

### Batch 1 — Contracts and infrastructure ports

- provider-neutral adapter protocols;
- source-record/artifact contracts;
- validation result/error contracts;
- object-storage port;
- required repository ports;
- configuration extensions.

### Batch 2 — Persistence foundation

- migrations/schema required by approved IA-1B contracts;
- PostgreSQL repository implementations;
- source-artifact metadata;
- provenance persistence;
- object-storage adapter;
- integration test infrastructure.

### Batch 3 — Ingestion core

- execution orchestration;
- validation;
- normalization;
- identifier resolution;
- idempotency;
- quarantine/rejection;
- correction/supersession handling.

### Batch 4 — Provider adapters

- `ng_primary`;
- `global_primary`;
- provider-specific translation;
- provider contract tests;
- controlled fixtures.

### Batch 5 — Verification and operations

- end-to-end ingestion tests;
- reconciliation tests;
- observability;
- local setup;
- CI updates;
- documentation and verification report.

The exact batch boundaries may be adjusted if implementation dependencies require it, but related changes should remain reviewable and each completed batch must be committed coherently.

## 57. Implementation gate: database and object storage

IA-1C must not claim completion until:

- PostgreSQL persistence is real rather than a placeholder;
- object-storage persistence is real rather than a mock-only abstraction;
- source metadata and raw payload can be linked;
- canonical market observations can be persisted;
- provenance can be queried;
- idempotency constraints are enforced;
- correction/supersession is testable.

## 58. Implementation gate: provider independence

Before claiming completion:

- both adapters satisfy the same provider-neutral contract;
- no provider SDK import exists in domain/application packages;
- no provider marketing-name business branching exists;
- canonical contracts do not expose provider response schemas;
- provider-specific identifiers remain mappings;
- provider-specific adjustment semantics are translated.

## 59. Implementation gate: data quality

Before claiming completion:

- invalid records are not silently accepted;
- ambiguous identifiers are quarantinable;
- raw evidence survives failed normalization;
- duplicate ingestion is idempotent;
- corrected source records preserve prior evidence;
- temporal/as-of metadata remains distinguishable;
- adjusted/unadjusted status is explicit.

## 60. Implementation gate: provenance

For a representative accepted observation, the system must demonstrate:

```
canonical observation
→ source record
→ raw artifact
→ ingestion execution/request
→ adapter/provider identity
```

The reverse relationship should also support investigation from a source artifact to affected canonical records where practical.

## 61. Implementation gate: CI

The exact implementation HEAD must have:

- CI triggered by the push;
- backend checks passing;
- frontend checks passing;
- IA-1C tests passing;
- no unresolved required CI failures.

The verification report must identify:

1. exact HEAD SHA;
2. workflow run ID;
3. job results;
4. test counts where available;
5. any limitations or non-gating external integration tests.

## 62. Implementation gate: second-engine review

Before IA-1C is declared complete, a second independent implementation/review pass should inspect:

- provider boundary;
- persistence boundary;
- temporal semantics;
- provenance;
- idempotency;
- correction handling;
- provider independence;
- credential handling;
- CI behavior;
- tests.

Any disagreement with the accepted architecture must be resolved before milestone closure.

## 63. Explicit non-decisions

IA-1C does not decide:

- exact ORM;
- exact migration tool;
- exact object-storage product;
- exact SDK versus HTTP implementation;
- exact provider request schedules;
- production provider contract;
- redistribution licensing;
- complete multi-asset model;
- portfolio valuation methodology;
- corporate-action adjustment algorithm beyond required ingestion semantics;
- AI interpretation behavior.

These remain separate decisions unless implementation makes one unavoidable.

## 64. Prohibited shortcuts

IA-1C must not:

- hard-code provider APIs into domain models;
- store only normalized data and discard raw evidence;
- use PostgreSQL as a substitute for the object-storage raw-artifact contract without an explicit ADR;
- silently treat adjusted prices as raw prices;
- use current provider symbols as permanent canonical identity;
- silently overwrite corrected data;
- bypass validation because a provider is considered authoritative;
- require live external providers for ordinary CI;
- expose provider credentials through APIs;
- introduce a generic financial chatbot;
- introduce stock-price prediction;
- implement trading execution.

## 65. Acceptance criteria

IA-1C is accepted only when all applicable criteria are satisfied:

### Architecture
- [ ] provider adapter boundary implemented;
- [ ] stable adapter IDs used;
- [ ] domain/application provider independent;
- [ ] raw storage abstraction provider/storage-vendor independent.

### Data
- [ ] source records retained;
- [ ] immutable raw artifacts retained;
- [ ] canonical market observations persisted;
- [ ] corporate-action ingestion boundary established;
- [ ] identifier mappings explicit;
- [ ] temporal/as-of semantics preserved;
- [ ] provenance queryable.

### Quality
- [ ] validation implemented;
- [ ] quarantine/rejection implemented;
- [ ] idempotency enforced;
- [ ] correction/supersession supported;
- [ ] adjusted/unadjusted semantics explicit.

### Providers
- [ ] Kobo adapter implemented behind `ng_primary`;
- [ ] EODHD adapter implemented behind `global_primary`;
- [ ] both satisfy shared adapter contract;
- [ ] provider-specific behavior isolated;
- [ ] current access/licensing assumptions verified for intended integration use.

### Persistence
- [ ] PostgreSQL repository implementation works;
- [ ] object storage implementation works;
- [ ] reconciliation/incomplete-state behavior tested.

### Testing
- [ ] unit tests;
- [ ] adapter contract tests;
- [ ] repository integration tests;
- [ ] object-storage integration tests;
- [ ] deterministic end-to-end fixture tests;
- [ ] CI passes on exact final HEAD.

### Governance
- [ ] secrets protected;
- [ ] raw provenance preserved;
- [ ] operational failures auditable;
- [ ] second-engine review completed;
- [ ] verification report committed.

## 66. Traceability

IA-1C implements or advances the following IA-1A/IA-1B requirements:

| Requirement area | IA-1C treatment |
|---|---|
| Provider independence | Adapter boundary and provider-neutral contracts |
| Security/listing identity | Identifier-resolution pipeline |
| Market observations | Retrieval, validation, normalization, persistence |
| Corporate actions | Event ingestion boundary |
| Temporal semantics | Observation/effective/available/ingested timestamps |
| Provenance | Source artifact → canonical lineage |
| Data quality | Validation, quarantine, rejection, state transitions |
| Raw vs canonical | Separate artifact and canonical persistence |
| Idempotency | Source identity/content-based replay protection |
| Corrections | Immutable raw evidence + supersession |
| Repository contracts | IA-1B persistence boundary |
| Auditability | Execution/request/provenance metadata |
| Provider licensing | Pre-production verification gate |

## 67. Next gate

The next step after this specification is **review and approval of IA-1C**, not provider SDK implementation.

After approval:

1. freeze the reviewed IA-1C contract;
2. verify current provider documentation/access requirements;
3. confirm implementation-specific persistence choices that were intentionally deferred;
4. implement in coherent batches;
5. commit each batch;
6. verify CI on each resulting HEAD;
7. run the second-engine review before declaring IA-1C complete.

**No provider-specific application code should be introduced before the IA-1C specification is approved and the implementation gate is opened.**


## 68. Explicit Per-Batch Implementation Gate

The criteria below are mandatory pass/fail gates for **every implementation batch**, not only the final IA-1C batch. They supplement Sections 57–62 and do not replace them.

### 68.1 Batch CI gate — PASS/FAIL

For each IA-1C implementation batch:

- [ ] the batch is committed as a coherent, reviewable commit;
- [ ] the exact resulting HEAD SHA is identified;
- [ ] CI is triggered for that exact HEAD under the repository's existing workflow;
- [ ] all required CI jobs for that HEAD pass;
- [ ] no subsequent IA-1C implementation batch begins until this batch's CI result is verified;
- [ ] the batch verification records the HEAD SHA, workflow run ID, job results, and any non-gating limitations.

**PASS condition:** all boxes above are satisfied.  
**FAIL condition:** any required check is absent, failing, unverified, or the next IA-1C implementation batch begins before verification.

### 68.2 Real integration-service gate — PASS/FAIL

Repository and object-storage integration tests must exercise **real service instances**, not only mocks or in-process substitutes:

- [ ] PostgreSQL integration tests run against a real PostgreSQL service instance;
- [ ] object-storage integration tests run against a real S3-compatible service instance selected for CI/local integration testing;
- [ ] the test suite proves startup, connection, persistence, retrieval, isolation, and teardown against those services;
- [ ] unit-level mocks remain permitted for unit tests but cannot substitute for these integration-service tests;
- [ ] the selected CI service implementation is deterministic and documented.

The current ADR direction remains unchanged: s3mock is the leading CI candidate, with MinIO suitable for fuller local development and moto remaining an alternative where appropriate. The exact implementation product remains an infrastructure choice under Section 63.

**PASS condition:** both real PostgreSQL and real S3-compatible integration-service tests pass in CI.  
**FAIL condition:** either persistence boundary is tested only with mocks/in-process substitutes, or either required real-service integration suite fails.

### 68.3 Idempotency invariant gate — PASS/FAIL

Idempotency must be demonstrated, not merely implemented or described.

A required CI test must:

1. execute the same logical ingestion/source fixture;
2. persist the resulting canonical state;
3. execute the same ingestion again;
4. verify that the second execution does not create duplicate authoritative observations;
5. verify that the resulting canonical state is equivalent to the state after the first execution;
6. verify that raw-artifact/provenance behavior remains consistent with the approved correction/idempotency contract.

**PASS condition:** the invariant test passes in CI and demonstrates repeat-ingestion stability.  
**FAIL condition:** idempotency is asserted only by implementation inspection, a unit helper test, or an unexecuted/manual scenario.

### 68.4 Quarantine classification gate — PASS/FAIL

Quarantine behavior must be tested for at least two distinct failure classes:

1. **Malformed/schema-invalid payload**
   - e.g. missing required structural field, invalid payload shape, or unparsable required field.

2. **Semantically invalid payload**
   - structurally parseable but violates a domain/data-quality invariant, such as impossible OHLC relationships or an otherwise invalid canonical mapping.

For both cases:

- [ ] raw evidence is retained;
- [ ] the record is not promoted to authoritative canonical data;
- [ ] quarantine state is persisted/observable where quarantine is the applicable outcome;
- [ ] the failure reason is explicit;
- [ ] the reason distinguishes malformed/schema-invalid from semantically invalid;
- [ ] the distinction is asserted by automated tests running in CI.

**PASS condition:** both failure classes are independently exercised and the automated assertions prove distinguishable quarantine reasons and non-promotion.  
**FAIL condition:** either class is untested, reasons are indistinguishable, raw evidence is lost, or the invalid record can reach authoritative canonical state.

### 68.5 Gate precedence and batch closure

These four gates are mandatory additions to the existing implementation gates.

A batch may be **implemented** without being **closed**.

A batch is **closed** only when:

```
Batch implementation
        ↓
Commit exact HEAD
        ↓
Batch CI gate PASS
        ↓
Required integration-service tests PASS
        ↓
Required invariant/classification tests PASS
        ↓
Verification recorded
        ↓
Next batch may begin
```

The final IA-1C milestone still requires all applicable Sections 57–62 gates and Section 65 acceptance criteria.

## 69. Traceability of the gate amendment

This amendment closes four consistency-review findings without changing architecture:

| Review finding | Explicit gate closure |
|---|---|
| Intermediate batches were not explicitly CI-gated | §68.1 requires CI verification before the next batch |
| Real PostgreSQL/S3-compatible services were not mandatory | §68.2 requires both real integration services |
| Idempotency was not required as a demonstrated invariant | §68.3 requires a repeat-ingestion invariant test |
| Malformed vs semantic quarantine was not explicitly distinguished in tests | §68.4 requires both classes and distinguishable reasons |

No new provider, storage, persistence, or CI architecture decision is introduced by this amendment.

## 70. Next gate

The next step after this amended specification is **narrow consistency re-review and approval of IA-1C**, not implementation.

After closure:

1. freeze the amended IA-1C contract;
2. open IA-1C Batch 1;
3. draft Batch 1 interface contracts and ports for review;
4. commit the approved Batch 1 as one coherent batch;
5. verify CI and the applicable per-batch gates on its exact HEAD before Batch 2 begins.
