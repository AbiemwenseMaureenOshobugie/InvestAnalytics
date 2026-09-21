# ADR-IA-1C-002: Raw Market-Data Record Storage

- Status: Accepted
- Date: 2026-09-20
- Scope: IA-1C Market Data Ingestion Foundation

## Context

IA-1B requires raw/source data and canonical data to remain distinguishable and requires durable, queryable provenance sufficient for historical reproducibility and audit.

A provider's raw response may contain fields, metadata, or representations that should not become part of the canonical domain model. Raw payloads therefore need an independent storage boundary.

## Decision

Use a hybrid raw-record architecture:

1. PostgreSQL stores raw-record metadata and provenance metadata.
2. Object storage stores the immutable raw payload/artifact.

The application-facing storage contract must be provider- and storage-vendor-independent. It should express operations such as store(payload) -> source_artifact_reference and retrieve(source_artifact_reference) -> payload rather than exposing S3/MinIO APIs to the domain or application layers.

### PostgreSQL metadata

At minimum, the metadata boundary will support:

- source/provider internal identifier;
- request/execution identity;
- retrieval timestamp;
- provider/source record identity where available;
- content hash;
- payload media/content type;
- object-storage reference;
- ingestion status;
- validation status;
- provenance linkage;
- retention/lifecycle metadata.

The exact relational schema remains an IA-1C implementation concern and must follow the IA-1B persistence contracts.

### Object storage

The raw payload is retained as an immutable source artifact. Re-ingestion or correction must create a new artifact/version or otherwise preserve the prior artifact according to the final retention contract. Existing raw evidence must not be silently overwritten.

## Local development and CI

For IA-1C implementation, local object storage should use an S3-compatible service rather than embedding an S3 vendor into the application boundary.

The initial test strategy should prefer a lightweight CI-compatible implementation. s3mock is the default candidate for repository integration tests because it provides an actual HTTP/S3 interaction boundary without requiring a full production object-storage stack.

Moto remains an alternative if Python-native mocking proves more reliable for specific tests.

For local developer workflows, MinIO is the preferred fuller S3-compatible service when developers need a persistent object-storage environment. LocalStack remains an alternative where AWS-service parity becomes necessary.

These are infrastructure/test choices, not domain contracts.

## Alternatives considered

### PostgreSQL only

Rejected as the primary raw-payload boundary because raw provider artifacts are better represented as immutable objects, while relational storage should hold queryable metadata and provenance.

### Object storage only

Rejected because ingestion status, provenance relationships, source identity, and operational queries need durable relational metadata.

### S3-specific application contract

Rejected because it would leak an infrastructure/vendor protocol into application and domain boundaries.

## Consequences

Positive:
- Raw evidence remains reproducible and separately addressable.
- PostgreSQL remains optimized for metadata, relationships, status, and queries.
- Storage vendor can change without changing domain contracts.
- Provider responses can be retained without forcing their schema into canonical entities.

Tradeoffs:
- IA-1C requires two persistence mechanisms.
- Local and CI environments need an object-storage test strategy.
- Retention, encryption, lifecycle, and access-control rules must be implemented deliberately.

## Follow-up

IA-1C implementation must define the exact source-artifact metadata contract, object-key strategy, hashing/idempotency rules, retention behavior, and integration tests before provider ingestion is considered complete.
