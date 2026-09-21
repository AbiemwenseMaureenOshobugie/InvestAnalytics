# ruff: noqa: E501
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.market_data.identifiers import SourceIdentity
from app.domain.market_data.observations import MarketObservation
from app.infrastructure.persistence.sqlalchemy_repositories import (
    SqlAlchemyMarketObservationRepository,
)


def test_market_observation_repository_is_importable() -> None:
    assert SqlAlchemyMarketObservationRepository is not None


def test_market_observation_domain_round_trip_shape() -> None:
    observation = MarketObservation(
        listing_id="listing-1",
        observed_at=datetime(2026, 1, 1, tzinfo=UTC),
        available_at=None,
        open=Decimal("10"),
        high=Decimal("11"),
        low=Decimal("9"),
        close=Decimal("10.5"),
        volume=Decimal("100"),
        currency="NGN",
        frequency="1d",
        adjusted=False,
        source_identity=SourceIdentity("ng_primary", "record-1"),
    )
    assert observation.close == Decimal("10.5")
    assert observation.source_identity.provider_id == "ng_primary"
