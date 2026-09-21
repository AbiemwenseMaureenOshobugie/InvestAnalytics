# IA-1C Batch 3 — Ingestion Core Contracts

**Status:** Revised draft for final signature review. Not yet implemented.  
**Depends on:** IA-1C specification §§56–68, ADR-IA-1C-001, ADR-IA-1C-002, ADR-IA-1C-003, IA-1C Batch 1 contracts, IA-1C Batch 2 persistence layer.  
**Scope:** Ingestion core only. No provider adapters, Kobo Terminal, EODHD, scheduler, API endpoint, or AI integration.

---

## 1. Boundary

Batch 3 implements the provider-neutral ingestion core.

It consumes the existing `MarketDataProviderPort`, retrieves immutable raw evidence through `RawArtifactStore`, validates source payloads, resolves canonical identifiers, normalizes accepted market data, applies source-replay and canonical-observation identity rules, persists record-level outcomes, records corrections through `Supersession`, and produces a deterministic execution summary.

Batch 3 does **not**:

- implement a provider adapter;
- call an external provider API;
- import a provider SDK or HTTP client;
- contain Kobo Terminal or EODHD logic;
- define provider-specific pagination, rate limiting, or authentication;
- add a scheduler, CLI, FastAPI ingestion endpoint, frontend, or AI integration.

Provider adapters remain Batch 4.

---

## 2. Contract list

| # | Contract | Kind | Location |
|---|---|---|---|
| 1 | `IngestionRequest` | value object | `domain/market_data/ingestion.py` |
| 2 | `IngestionExecution` | entity | `domain/market_data/ingestion.py` |
| 3 | `IngestionExecutionStatus` | enum | `domain/market_data/ingestion.py` |
| 4 | `RecordOutcomeKind` | enum | `domain/market_data/ingestion.py` |
| 5 | `RecordOutcome` | value object | `domain/market_data/ingestion.py` |
| 6 | `IngestionResult` | value object | `domain/market_data/ingestion.py` |
| 7 | `SourcePayload` | value object | `domain/market_data/ingestion.py` |
| 8 | `SourceReplayIdentity` | value object | `domain/market_data/ingestion.py` |
| 9 | `ObservationIdentity` | value object | `domain/market_data/ingestion.py` |
| 10 | `IdempotencyState` | enum | `domain/market_data/ingestion.py` |
| 11 | `IdempotencyResult` | value object | `domain/market_data/ingestion.py` |
| 12 | `ValidationContext` | value object | `domain/market_data/quality.py` |
| 13 | `QuarantineRecord` | entity | `domain/market_data/quality.py` |
| 14 | `IdentifierResolutionState` | enum | `domain/market_data/identifiers.py` |
| 15 | `IdentifierResolutionResult` | value object | `domain/market_data/identifiers.py` |
| 16 | `NormalizationResult` | value object | `domain/market_data/observations.py` |
| 17 | `Supersession` | entity | `domain/market_data/corrections.py` |
| 18 | `SchemaValidator` | Protocol | `application/ports/validation.py` |
| 19 | `SemanticValidator` | Protocol | `application/ports/validation.py` |
| 20 | `CrossRecordValidator` | Protocol | `application/ports/validation.py` |
| 21 | `IdentifierResolver` | Protocol | `application/ports/ingestion.py` |
| 22 | `MarketDataNormalizer` | Protocol | `application/ports/ingestion.py` |
| 23 | `IdempotencyService` | Protocol | `application/ports/ingestion.py` |
| 24 | `IngestionService` | Protocol | `application/ports/ingestion.py` |
| 25 | `IngestionExecutionRepositoryPort` | Protocol | `application/ports/repositories.py` |
| 26 | `QuarantineRepositoryPort` | Protocol | `application/ports/repositories.py` |
| 27 | `SupersessionRepositoryPort` | Protocol | `application/ports/repositories.py` |

Existing Batch 1 types reused:

- `SourceRecord`
- `SourceIdentity`
- `MarketObservation`
- `ValidationResult`, `ValidationState`, `ValidationCategory`, `ValidationSeverity`, `ValidationIssue`
- `ProviderError`, `PersistenceError`
- `MarketDataProviderPort`
- `RawArtifactStore`
- existing repository ports for canonical entities and source records.

The contract list deliberately separates **source replay identity** from **canonical observation identity**.

---

## 3. Identity model

Batch 3 must not use provider source identity as canonical observation identity.

### 3.1 Source replay identity

This answers:

> Have I already processed this exact provider/source record?

```python
@dataclass(frozen=True)
class SourceReplayIdentity:
    provider_id: str
    source_record_id: str
```

A repeated source record with the same content hash is a duplicate replay.

### 3.2 Canonical observation identity

This answers:

> Does this record represent the same logical market observation?

```python
@dataclass(frozen=True)
class ObservationIdentity:
    listing_id: str
    observed_at: datetime
    frequency: str
    adjusted: bool
```

Provider/source identifiers are provenance/evidence attributes, not the sole definition of canonical observation identity.

The exact multi-provider conflict policy is governed by the canonical observation persistence contract and must not be invented by a provider adapter.

### 3.3 Identity outcomes

```text
same source identity
    + same content hash
        -> DUPLICATE

same source identity
    + different content hash
        -> CORRECTION / SOURCE REPLAY CONFLICT

different source identity
    + different observation identity
        -> NEW

different source identity
    + same observation identity
    + equivalent canonical content
        -> DUPLICATE / EQUIVALENT

different source identity
    + same observation identity
    + changed canonical content
        -> CORRECTION
        -> SUPersession link
```

A correction must preserve the previous source evidence. Raw artifacts are immutable.

---

## 4. Domain signatures

### 4.1 Ingestion request and execution

```python
class IngestionExecutionStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass(frozen=True)
class IngestionRequest:
    adapter_id: str
    listing_ids: tuple[str, ...]
    start: datetime
    end: datetime
    frequency: str
    adjusted: bool


@dataclass(frozen=True)
class IngestionExecution:
    execution_id: str
    adapter_id: str
    started_at: datetime
    completed_at: datetime | None
    status: IngestionExecutionStatus
    request_count: int
    source_record_count: int
    accepted_count: int
    quarantined_count: int
    rejected_count: int
    error_count: int
    retry_count: int
```

`request_count` means the number of provider-neutral retrieval requests issued by the ingestion core, not simply the number of listings.

### 4.2 Record outcome

```python
class RecordOutcomeKind(StrEnum):
    ACCEPTED = "accepted"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"
    CORRECTION = "correction"
    ERROR = "error"


@dataclass(frozen=True)
class RecordOutcome:
    source_record_id: str
    kind: RecordOutcomeKind
    canonical_observation_id: str | None
    quarantine_id: str | None
    supersession_id: str | None
    error_message: str | None
```

Record outcomes are durable independently of the aggregate execution status.

### 4.3 Ingestion result

```python
@dataclass(frozen=True)
class IngestionResult:
    execution: IngestionExecution
    outcomes: tuple[RecordOutcome, ...]
```

### 4.4 Source payload

```python
@dataclass(frozen=True)
class SourcePayload:
    record: SourceRecord
    payload: bytes
```

`SourceRecord` remains metadata/identity. The raw bytes are retrieved through `RawArtifactStore` using the record's artifact reference and are passed to the validation/normalization boundary without exposing storage-vendor details.

### 4.5 Idempotency

```python
class IdempotencyState(StrEnum):
    NEW = "new"
    DUPLICATE = "duplicate"
    CORRECTION = "correction"


@dataclass(frozen=True)
class IdempotencyResult:
    state: IdempotencyState
    existing_observation_id: str | None
    existing_source_record_id: str | None
    reason: str | None
```

The idempotency contract operates on both source replay identity and canonical observation identity; it must not collapse them into one key.

### 4.6 Identifier resolution

```python
class IdentifierResolutionState(StrEnum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


@dataclass(frozen=True)
class IdentifierResolutionResult:
    state: IdentifierResolutionState
    listing_id: str | None
    security_id: str | None
    mapping_id: str | None
    reason: str | None
```

An unresolved or ambiguous identifier must not be silently converted into a canonical listing.

### 4.7 Quarantine

```python
@dataclass(frozen=True)
class QuarantineRecord:
    quarantine_id: str
    source_record_id: str
    state: ValidationState
    category: ValidationCategory
    reason_code: str
    reason: str
    quarantined_at: datetime
```

Quarantine preserves the raw evidence reference through the source record. It does not create an authoritative canonical observation.

### 4.8 Supersession

```python
@dataclass(frozen=True)
class Supersession:
    supersession_id: str
    previous_source_record_id: str
    replacement_source_record_id: str
    reason: str
    created_at: datetime
```

Supersession is a separate domain entity and is persisted through its own repository port.

### 4.9 Normalization

```python
@dataclass(frozen=True)
class NormalizationResult:
    observation: MarketObservation | None
    issues: tuple[ValidationIssue, ...]
    transformation_version: str
```

Normalization must preserve the canonical temporal fields and adjusted/unadjusted semantics defined by Batch 1.

### 4.10 Validation context

```python
@dataclass(frozen=True)
class ValidationContext:
    contract_version: str
    received_at: datetime
```

---

## 5. Application port signatures

### 5.1 Three validators

Decision 2B freezes three distinct validator protocols.

```python
class SchemaValidator(Protocol):
    def validate(
        self,
        source: SourcePayload,
        context: ValidationContext,
    ) -> ValidationResult:
        ...


class SemanticValidator(Protocol):
    def validate(
        self,
        source: SourcePayload,
        context: ValidationContext,
    ) -> ValidationResult:
        ...


class CrossRecordValidator(Protocol):
    def validate(
        self,
        records: tuple[SourcePayload, ...],
        context: ValidationContext,
    ) -> tuple[ValidationResult, ...]:
        ...
```

Schema validation addresses source structure and required representation.

Semantic validation addresses record-level meaning and deterministic market-data invariants.

Cross-record validation addresses relationships among the supplied records. It does **not** infer trading-calendar completeness unless a separately approved market-calendar contract exists.

The returned cross-record results correspond to the supplied records in the same order.

### 5.2 Identifier resolution

```python
class IdentifierResolver(Protocol):
    def resolve(
        self,
        source_identity: SourceIdentity,
    ) -> IdentifierResolutionResult:
        ...
```

### 5.3 Normalization

```python
class MarketDataNormalizer(Protocol):
    def normalize(
        self,
        source: SourcePayload,
        resolution: IdentifierResolutionResult,
    ) -> NormalizationResult:
        ...
```

Provider response models do not cross this boundary.

### 5.4 Idempotency

```python
class IdempotencyService(Protocol):
    def check(
        self,
        source_identity: SourceReplayIdentity,
        observation_identity: ObservationIdentity,
        content_hash: str,
    ) -> IdempotencyResult:
        ...
```

The service must distinguish:

1. same source identity + same content;
2. same source identity + changed content;
3. different source identity + new canonical observation;
4. different source identity + same canonical observation + equivalent content;
5. different source identity + same canonical observation + changed content.

### 5.5 Ingestion orchestration

```python
class IngestionService(Protocol):
    def ingest(
        self,
        request: IngestionRequest,
    ) -> IngestionResult:
        ...
```

The implementation lives in `application/market_data/ingestion.py`.

It imports domain types and application ports only.

---

## 6. Ingestion orchestration

The provider-neutral flow is:

```text
IngestionRequest
      |
      v
IngestionExecution
      |
      v
MarketDataProviderPort
      |
      v
SourceRecord + raw artifact reference
      |
      +----> RawArtifactStore.retrieve()
      |
      v
SourcePayload
      |
      +----> SchemaValidator
      |
      +----> SemanticValidator
      |
      +----> CrossRecordValidator
      |
      +----> IdentifierResolver
      |
      v
MarketDataNormalizer
      |
      v
Source replay identity
      |
      +----> duplicate -> durable DUPLICATE outcome / no-op
      |
      v
Canonical observation identity
      |
      +----> new -> persist canonical observation
      |
      +----> changed existing -> correction + Supersession
      |
      v
Provenance
      |
      v
Record outcome
      |
      v
IngestionExecution aggregate
```

Raw evidence must be retained even when validation, resolution, or normalization fails.

The ingestion core does not know whether the raw artifact is stored in S3, MinIO, s3mock, or another implementation.

---

## 7. Persistence ports

The following ports extend Batch 2's repository boundary.

```python
class IngestionExecutionRepositoryPort(Protocol):
    def save(self, execution: IngestionExecution) -> None:
        ...

    def get(self, execution_id: str) -> IngestionExecution | None:
        ...


class QuarantineRepositoryPort(Protocol):
    def save(self, record: QuarantineRecord) -> None:
        ...

    def get(self, quarantine_id: str) -> QuarantineRecord | None:
        ...

    def find_by_source_record(
        self,
        source_record_id: str,
    ) -> tuple[QuarantineRecord, ...]:
        ...


class SupersessionRepositoryPort(Protocol):
    def save(self, supersession: Supersession) -> None:
        ...

    def find_by_replacement(
        self,
        replacement_source_record_id: str,
    ) -> Supersession | None:
        ...

    def find_by_previous(
        self,
        previous_source_record_id: str,
    ) -> tuple[Supersession, ...]:
        ...
```

Batch 3 will add the required migration/schema for these durable outcomes.

The existing Batch 2 market-observation persistence identity must not be treated as the complete application-level correction model; Batch 3 must establish the explicit source/canonical/supersession semantics above.

---

## 8. Record-level durability and execution atomicity

Decision 1B is frozen:

> Record outcomes are durable independently; execution status summarizes the aggregate.

A failed record does not roll back unrelated successful records.

The implementation should use transaction boundaries that preserve this property.

### Execution status rules

| Condition | Status |
|---|---|
| At least one accepted and no quarantine/rejection/error | `COMPLETED` |
| At least one accepted plus any quarantine/rejection/error | `PARTIAL` |
| Zero accepted, one or more quarantine/rejection, no unrecovered execution error | `PARTIAL` |
| Zero accepted and one or more unrecovered execution/processing errors | `FAILED` |
| Provider fetch/execution failure prevents completion of the execution | `FAILED` |

The rule is deterministic:

- `FAILED` means the execution itself could not complete successfully.
- `PARTIAL` means the execution completed but its record population contains non-success outcomes.
- `COMPLETED` means every processed record reached an accepted outcome.

A provider failure after some records have already been durably processed results in `PARTIAL` if the execution can be closed with a truthful aggregate summary; otherwise it is `FAILED`. The implementation must record the execution error rather than silently converting it to a record rejection.

---

## 9. Correction and supersession rules

Corrections follow these rules:

1. Raw artifacts are immutable.
2. Existing source records remain retrievable.
3. A corrected source payload is represented by new evidence.
4. If the corrected evidence represents an existing canonical observation, it is not silently overwritten.
5. A `Supersession` entity links previous and replacement source records.
6. Provenance remains queryable for both previous and replacement evidence.
7. A correction must not destroy the historical evidence required to reproduce the prior state.

The canonical persistence/versioning mechanism must preserve the distinction between:

- source evidence;
- canonical observation state;
- supersession relationship.

---

## 10. Quarantine and rejection

The Batch 3 classification rule is:

### Rejected

The system can deterministically establish that the source record cannot enter the canonical ingestion pipeline.

Examples:

- malformed/unparseable source representation;
- impossible required field representation;
- structurally invalid record;
- deterministic semantic invariant violation where the record is known invalid.

### Quarantined

The system cannot safely establish authoritative canonical status, but the raw evidence must be retained for investigation or later reprocessing.

Examples:

- unresolved identifier;
- ambiguous identifier mapping;
- unsupported or ambiguous adjustment semantics;
- insufficient information to determine authoritative interpretation.

Exact reason codes must be deterministic and test-covered.

---

## 11. Cross-record validation scope

`CrossRecordValidator` operates on the records supplied to one validation operation.

It may detect:

- duplicate logical timestamps within the supplied set;
- conflicting records for the same logical observation;
- incompatible frequency/period alignment;
- contradictory values for otherwise identical source/canonical identity;
- other explicitly defined cross-record invariants.

It does **not** declare a missing trading-calendar observation invalid merely because a timestamp is absent.

Trading-calendar completeness requires an explicit market-calendar/reference-data contract and is outside this Batch 3 contract.

---

## 12. Acceptance tests

All required tests must pass in CI.

### Validation

- malformed source payload → rejected with `MALFORMED`;
- semantically invalid OHLC → deterministic `SEMANTIC` classification;
- valid source payload → accepted;
- cross-record contradiction → flagged by `CrossRecordValidator`;
- raw payload is retrievable through the storage port before validation;
- malformed payload reaches schema validation without provider-specific code.

### Identifier resolution

- known mapping → `RESOLVED`;
- unknown mapping → `UNRESOLVED`;
- conflicting mappings → `AMBIGUOUS`;
- superseded mapping → explicit `SUPERSEDED` handling;
- unresolved/ambiguous records do not produce authoritative canonical observations.

### Normalization

- identical fixture → deterministic identical canonical result;
- adjusted flag preserved;
- observed/available temporal semantics preserved;
- provider-specific field names absent from canonical output;
- transformation version recorded.

### Source replay and idempotency

- same source identity + same hash → one durable canonical outcome;
- same source identity + changed hash → correction/replay conflict is explicit;
- different source identity + different observation identity → new observation;
- different source identity + same observation identity + changed content → correction;
- concurrent/repeated ingestion cannot create duplicate authoritative canonical state.

### Quarantine

- invalid source → raw artifact retained;
- quarantine record created;
- no authoritative canonical observation created;
- `MALFORMED` and `SEMANTIC` reason codes remain distinguishable.

### Supersession

- correction creates a `Supersession` record;
- previous source record remains retrievable;
- replacement source record remains retrievable;
- supersession direction is correct;
- provenance remains available for both source records.

### Execution

- 95 accepted + 3 quarantined + 2 rejected → `PARTIAL`;
- all accepted → `COMPLETED`;
- zero accepted + only quarantine/rejection → `PARTIAL`;
- unrecovered provider/execution failure → `FAILED`;
- record-level failure does not roll back unrelated successful records;
- execution counts equal durable record outcomes.

### Provenance

The following chain must be queryable:

```text
canonical observation
    -> source record
    -> raw artifact
    -> ingestion execution/request
    -> adapter/provider identity
```

For corrections, the previous and replacement evidence must both remain traceable.

### Dependency direction

Automated boundary checks must establish:

- `domain/` contains no SQLAlchemy, boto3, HTTP, provider SDK, or provider endpoint imports;
- `application/market_data/` imports domain types and application ports, not infrastructure implementations;
- provider-specific modules do not exist in Batch 3;
- storage implementation details remain behind `RawArtifactStore`;
- PostgreSQL implementation remains behind repository ports.

---

## 13. Batch 3 implementation boundary

Batch 3 implementation may include:

- domain contract additions described in this document;
- application ingestion ports;
- validator implementations;
- identifier-resolution implementation against existing repository ports;
- normalization implementation for the provider-neutral market-data contract;
- idempotency/correction orchestration;
- ingestion execution orchestration;
- PostgreSQL persistence for execution, quarantine, and supersession;
- migrations required for those durable records;
- unit, integration, invariant, and end-to-end fixture tests;
- CI adjustments required to execute those tests.

Batch 3 must not include provider adapters.

---

## 14. Final pre-implementation gate

Before Batch 3 code is written, this document must receive final signature review.

The signatures are considered frozen only after approval of:

1. source replay identity versus canonical observation identity;
2. raw payload access through `RawArtifactStore`;
3. three-validator separation;
4. deterministic execution status rules;
5. record-level durability;
6. explicit correction/supersession semantics;
7. quarantine versus rejection classification;
8. repository ports and transaction boundaries.

After approval:

1. implement Batch 3 as one coherent batch;
2. commit the complete batch without history rewriting;
3. run CI on the exact resulting HEAD;
4. do not proceed to Batch 4 until the Batch 3 implementation gate is green and verified.
