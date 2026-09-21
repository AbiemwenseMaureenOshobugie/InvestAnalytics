"""Domain identifiers for externally sourced market data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityIdentifier:
    value: str
    scheme: str


@dataclass(frozen=True)
class ListingIdentifier:
    value: str
    scheme: str


@dataclass(frozen=True)
class SourceIdentity:
    provider_id: str
    source_record_id: str
