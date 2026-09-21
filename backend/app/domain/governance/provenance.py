"""Provenance domain contract required by IA-1C persistence ports."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Provenance:
    provenance_id: str
    source_record_id: str
    transformation_version: str
