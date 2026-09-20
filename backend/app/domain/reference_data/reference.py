"""Minimal reference-data domain contracts required by IA-1C repository ports."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Security:
    security_id: str


@dataclass(frozen=True)
class Listing:
    listing_id: str
    security_id: str


@dataclass(frozen=True)
class IdentifierMapping:
    provider_id: str
    external_identifier: str
    canonical_identifier: str
