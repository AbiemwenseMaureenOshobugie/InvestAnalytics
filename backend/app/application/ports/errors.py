"""Provider-neutral error classification contracts."""

from enum import StrEnum


class ProviderFailureKind(StrEnum):
    RETRYABLE = "retryable"
    NON_RETRYABLE = "non_retryable"
    UNKNOWN = "unknown"


class PersistenceFailureKind(StrEnum):
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNAVAILABLE = "unavailable"
    INTEGRITY_VIOLATION = "integrity_violation"
    TRANSIENT = "transient"
    CONCURRENCY_CONFLICT = "concurrency_conflict"


class ProviderError(Exception):
    """Provider-neutral failure raised by an adapter boundary."""

    def __init__(self, message: str, kind: ProviderFailureKind) -> None:
        super().__init__(message)
        self.kind = kind


class PersistenceError(Exception):
    """Persistence failure exposed across the infrastructure boundary."""

    def __init__(self, message: str, kind: PersistenceFailureKind) -> None:
        super().__init__(message)
        self.kind = kind
