"""Application-facing persistence repository contracts."""

from datetime import datetime
from typing import Protocol

from app.domain.market_data.observations import MarketObservation
from app.domain.market_data.identifiers import SourceIdentity
from app.domain.market_data.reference import (
    CorporateAction,
    IdentifierMapping,
    Listing,
    Security,
)
from app.application.ports.market_data import SourceRecord
from app.domain.governance.provenance import Provenance


class SecurityRepositoryPort(Protocol):
    def get(self, security_id: str) -> Security | None:
        ...

    def save(self, security: Security) -> None:
        ...


class ListingRepositoryPort(Protocol):
    def get(self, listing_id: str) -> Listing | None:
        ...

    def save(self, listing: Listing) -> None:
        ...


class IdentifierMappingRepositoryPort(Protocol):
    def find(
        self,
        provider_id: str,
        external_identifier: str,
    ) -> IdentifierMapping | None:
        ...

    def save(self, mapping: IdentifierMapping) -> None:
        ...


class MarketObservationRepositoryPort(Protocol):
    def save(self, observation: MarketObservation) -> None:
        ...

    def find_existing(
        self,
        observation: MarketObservation,
    ) -> MarketObservation | None:
        ...

    def get_by_listing_and_period(
        self,
        listing_id: str,
        start: datetime,
        end: datetime,
    ) -> tuple[MarketObservation, ...]:
        ...

    def get_as_of(
        self,
        listing_id: str,
        observed_at: datetime,
        available_at: datetime,
    ) -> tuple[MarketObservation, ...]:
        ...


class CorporateActionRepositoryPort(Protocol):
    def save(self, action: CorporateAction) -> None:
        ...

    def get_by_listing_and_period(
        self,
        listing_id: str,
        start: datetime,
        end: datetime,
    ) -> tuple[CorporateAction, ...]:
        ...


class SourceRecordRepositoryPort(Protocol):
    def save(self, record: SourceRecord) -> None:
        ...

    def find_by_source_identity(
        self,
        identity: SourceIdentity,
    ) -> SourceRecord | None:
        ...


class ProvenanceRepositoryPort(Protocol):
    def save(self, provenance: Provenance) -> None:
        ...

    def get(self, provenance_id: str) -> Provenance | None:
        ...
