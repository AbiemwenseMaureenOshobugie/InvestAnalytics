# InvestAnalytics Documentation

This directory contains the foundational specifications, architecture decisions, and milestone contracts for the InvestAnalytics platform.

## Core Specifications

| Document | Description |
|----------|-------------|
| [PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md) | Foundational engineering principles and governance rules |
| [PRODUCT_CHARTER.md](PRODUCT_CHARTER.md) | Product identity, vision, users, scope, and milestones |
| [MASTER_CONTEXT.md](MASTER_CONTEXT.md) | Working context for development engines |
| [USER_SYSTEM_WORKFLOW_SPECIFICATION.md](USER_SYSTEM_WORKFLOW_SPECIFICATION.md) | 12 core user/system workflows |
| [DOMAIN_MODEL_SPECIFICATION.md](DOMAIN_MODEL_SPECIFICATION.md) | Conceptual domain model derived from workflows |
| [SYSTEM_ARCHITECTURE_SPECIFICATION.md](SYSTEM_ARCHITECTURE_SPECIFICATION.md) | Modular monolith architecture with layer boundaries |
| [IA-0A_IMPLEMENTATION_SKELETON_SPECIFICATION.md](IA-0A_IMPLEMENTATION_SKELETON_SPECIFICATION.md) | Implementation skeleton specification for IA-0A |
| [IA-1A_EQUITY_INTELLIGENCE_CORE_REQUIREMENTS.md](IA-1A_EQUITY_INTELLIGENCE_CORE_REQUIREMENTS.md) | IA-1A requirements, domain contracts, invariants, and implementation gates |
| [IA-1B_DATA_MODEL_PERSISTENCE_CONTRACTS.md](IA-1B_DATA_MODEL_PERSISTENCE_CONTRACTS.md) | IA-1B data model, persistence, temporal, provenance, and repository contracts |
| [IA-1C_PROVIDER_EVALUATION.md](IA-1C_PROVIDER_EVALUATION.md) | IA-1C market-data provider research and decision input |
| [IA-1C_MARKET_DATA_INGESTION_FOUNDATION_SPECIFICATION.md](IA-1C_MARKET_DATA_INGESTION_FOUNDATION_SPECIFICATION.md) | IA-1C provider adapters, raw records, ingestion, validation, normalization, provenance, and implementation gates |

## Architecture Decision Records

| ADR | Decision |
|-----|----------|
| [ADR-IA-1C-001_PROVIDER_SELECTION.md](decisions/ADR-IA-1C-001_PROVIDER_SELECTION.md) | First Nigerian and global market-data adapters |
| [ADR-IA-1C-002_RAW_RECORD_STORAGE.md](decisions/ADR-IA-1C-002_RAW_RECORD_STORAGE.md) | PostgreSQL metadata plus immutable raw object storage |
| [ADR-IA-1C-003_CI_GATING.md](decisions/ADR-IA-1C-003_CI_GATING.md) | CI runs on every push, including documentation-only commits |

## Verification Reports

Verification reports will be added as milestones are validated.
