"""Validation vocabulary for governed market-data ingestion."""

from dataclasses import dataclass
from enum import StrEnum


class ValidationState(StrEnum):
    ACCEPTED = "accepted"
    WARNING = "warning"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class ValidationCategory(StrEnum):
    MALFORMED = "malformed"
    SEMANTIC = "semantic"
    INTEGRITY = "integrity"
    TEMPORAL = "temporal"
    IDENTIFIER = "identifier"
    PROVENANCE = "provenance"


class ValidationSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    category: ValidationCategory
    severity: ValidationSeverity
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    state: ValidationState
    issues: tuple[ValidationIssue, ...]
    contract_version: str
