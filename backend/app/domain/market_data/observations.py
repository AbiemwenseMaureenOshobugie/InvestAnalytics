"""Canonical market-observation domain types."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .identifiers import SourceIdentity


@dataclass(frozen=True)
class MarketObservation:
    listing_id: str
    observed_at: datetime
    available_at: datetime | None
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    close: Decimal
    volume: Decimal | None
    currency: str
    frequency: str
    adjusted: bool
    source_identity: SourceIdentity
