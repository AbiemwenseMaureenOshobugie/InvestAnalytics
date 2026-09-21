# ruff: noqa: E501
import os
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.application.ports.market_data import SourceRecord
from app.config import get_settings
from app.domain.governance.provenance import Provenance
from app.domain.market_data.identifiers import SourceIdentity
from app.domain.market_data.observations import MarketObservation
from app.domain.reference_data.reference import Listing, Security
from app.infrastructure.persistence.database import DatabaseConnection
from app.infrastructure.persistence.sqlalchemy_repositories import (
    SqlAlchemyListingRepository,
    SqlAlchemyMarketObservationRepository,
    SqlAlchemyProvenanceRepository,
    SqlAlchemySecurityRepository,
    SqlAlchemySourceRecordRepository,
)
from app.infrastructure.storage.s3 import S3RawArtifactStore


def _require_integration_environment() -> None:
    required = ("DATABASE_URL", "RAW_STORAGE_ENDPOINT")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        if os.getenv("CI") == "true":
            pytest.fail(f"IA-1C integration environment missing: {', '.join(missing)}")
        pytest.skip("IA-1C real integration services are not configured locally")


@pytest.fixture()
def integration_context():
    _require_integration_environment()
    settings = get_settings()
    database = DatabaseConnection(settings)
    assert database.check()
    store = S3RawArtifactStore(settings)
    yield database, store


def test_real_postgresql_and_s3_round_trip(integration_context) -> None:
    database, store = integration_context
    security_repo = SqlAlchemySecurityRepository(database)
    listing_repo = SqlAlchemyListingRepository(database)
    source_repo = SqlAlchemySourceRecordRepository(database)
    provenance_repo = SqlAlchemyProvenanceRepository(database)
    observation_repo = SqlAlchemyMarketObservationRepository(database)

    suffix = os.getenv("GITHUB_RUN_ID", "local")
    security_repo.save(Security(f"security-integration-{suffix}"))
    listing_repo.save(Listing(f"listing-integration-{suffix}", f"security-integration-{suffix}"))

    payload = b'{"close":10.5,"currency":"NGN"}'
    artifact = store.store(
        payload, content_type="application/json", artifact_id=f"integration/{suffix}/artifact.json"
    )
    source = SourceRecord(
        adapter_id="ng_primary",
        source_identity=SourceIdentity("ng_primary", f"record-integration-{suffix}"),
        request_id=f"request-integration-{suffix}",
        retrieved_at=datetime.now(UTC),
        artifact_reference=artifact.artifact_id,
        content_hash=artifact.content_hash,
        content_type=artifact.content_type,
        validation_state="accepted",
    )
    source_repo.save(source)
    provenance_repo.save(Provenance(f"provenance-integration-{suffix}", source.source_identity.source_record_id, "ia1c-test-v1"))

    observation = MarketObservation(
        listing_id=f"listing-integration-{suffix}",
        observed_at=datetime(2026, 1, 2, tzinfo=UTC),
        available_at=datetime(2026, 1, 2, 16, tzinfo=UTC),
        open=Decimal("10"), high=Decimal("11"), low=Decimal("9"), close=Decimal("10.5"),
        volume=Decimal("100"), currency="NGN", frequency="1d", adjusted=False,
        source_identity=source.source_identity,
    )
    observation_repo.save(observation)
    assert observation_repo.find_existing(observation) == observation
    assert observation_repo.get_by_listing_and_period(
        observation.listing_id, datetime(2026, 1, 1, tzinfo=UTC), datetime(2026, 1, 3, tzinfo=UTC)
    ) == (observation,)
    assert store.retrieve(artifact).content == payload
    assert provenance_repo.get(f"provenance-integration-{suffix}") == Provenance(
        f"provenance-integration-{suffix}", source.source_identity.source_record_id, "ia1c-test-v1"
    )


def test_repeated_observation_ingestion_is_idempotent(integration_context) -> None:
    database, _ = integration_context
    suffix = os.getenv("GITHUB_RUN_ID", "local")
    security_repo = SqlAlchemySecurityRepository(database)
    listing_repo = SqlAlchemyListingRepository(database)
    observation_repo = SqlAlchemyMarketObservationRepository(database)

    security_repo.save(Security(f"security-idempotent-{suffix}"))
    listing_repo.save(Listing(f"listing-idempotent-{suffix}", f"security-idempotent-{suffix}"))
    observation = MarketObservation(
        listing_id=f"listing-idempotent-{suffix}",
        observed_at=datetime(2026, 2, 1, tzinfo=UTC),
        available_at=None,
        open=Decimal("20"), high=Decimal("21"), low=Decimal("19"), close=Decimal("20.5"),
        volume=Decimal("200"), currency="NGN", frequency="1d", adjusted=False,
        source_identity=SourceIdentity("ng_primary", f"record-idempotent-{suffix}"),
    )
    observation_repo.save(observation)
    observation_repo.save(observation)
    rows = observation_repo.get_by_listing_and_period(
        observation.listing_id, datetime(2026, 2, 1, tzinfo=UTC), datetime(2026, 2, 2, tzinfo=UTC)
    )
    assert rows == (observation,)
