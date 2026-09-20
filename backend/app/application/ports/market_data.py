"""Provider-neutral market-data application ports."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.domain.market_data.identifiers import (
    ListingIdentifier,
    SecurityIdentifier,
    SourceIdentity,
)
from app.domain.market_data.quality import ValidationState


@dataclass(frozen=True)
class ProviderCapabilities:
    supports_security_reference: bool
    supports_listing_reference: bool
    supports_market_observations: bool
    supports_corporate_actions: bool
    supports_identifier_resolution: bool
    supports_historical_data: bool
    supports_delisted_data: bool
    supports_pagination: bool
    supported_frequencies: tuple[str, ...]


@dataclass(frozen=True)
class SecurityReferenceRequest:
    identifiers: tuple[SecurityIdentifier, ...]


@dataclass(frozen=True)
class ListingReferenceRequest:
    identifiers: tuple[ListingIdentifier, ...]


@dataclass(frozen=True)
class MarketObservationRequest:
    listing_id: str
    start: datetime
    end: datetime
    frequency: str
    adjusted: bool


@dataclass(frozen=True)
class CorporateActionRequest:
    listing_id: str
    start: datetime
    end: datetime


@dataclass(frozen=True)
class SourceRecord:
    adapter_id: str
    source_identity: SourceIdentity
    request_id: str
    retrieved_at: datetime
    artifact_reference: str
    content_hash: str
    content_type: str
    validation_state: ValidationState


@dataclass(frozen=True)
class ProviderSourceResponse:
    records: tuple[SourceRecord, ...]


class MarketDataProviderPort(Protocol):
    @property
    def adapter_id(self) -> str:
        ...

    @property
    def capabilities(self) -> ProviderCapabilities:
        ...

    def get_security_reference(
        self,
        request: SecurityReferenceRequest,
    ) -> ProviderSourceResponse:
        ...

    def get_listing_reference(
        self,
        request: ListingReferenceRequest,
    ) -> ProviderSourceResponse:
        ...

    def get_market_observations(
        self,
        request: MarketObservationRequest,
    ) -> ProviderSourceResponse:
        ...

    def get_corporate_actions(
        self,
        request: CorporateActionRequest,
    ) -> ProviderSourceResponse:
        ...
