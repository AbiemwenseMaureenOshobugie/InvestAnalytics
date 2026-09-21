# ruff: noqa: E501
"""SQLAlchemy Core repository adapters for IA-1C."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.application.ports.errors import PersistenceError, PersistenceFailureKind
from app.application.ports.market_data import SourceRecord
from app.application.ports.repositories import (
    CorporateActionRepositoryPort,
    IdentifierMappingRepositoryPort,
    ListingRepositoryPort,
    MarketObservationRepositoryPort,
    ProvenanceRepositoryPort,
    SecurityRepositoryPort,
    SourceRecordRepositoryPort,
)
from app.domain.governance.provenance import Provenance
from app.domain.market_data.corporate_actions import CorporateAction
from app.domain.market_data.identifiers import SourceIdentity
from app.domain.market_data.observations import MarketObservation
from app.domain.reference_data.reference import IdentifierMapping, Listing, Security
from .database import DatabaseConnection

class SqlAlchemySecurityRepository(SecurityRepositoryPort):
    def __init__(self, database: DatabaseConnection) -> None: self.database = database
    def get(self, security_id: str) -> Security | None:
        with self.database.engine.connect() as connection:
            row = connection.execute(text("SELECT security_id FROM securities WHERE security_id=:id"), {"id": security_id}).mappings().first()
        return Security(str(row["security_id"])) if row else None
    def save(self, security: Security) -> None:
        try:
            with self.database.engine.begin() as connection:
                connection.execute(text("INSERT INTO securities(security_id) VALUES(:id) ON CONFLICT DO NOTHING"), {"id": security.security_id})
        except IntegrityError as exc:
            raise PersistenceError("Unable to persist security", PersistenceFailureKind.INTEGRITY_VIOLATION) from exc

class SqlAlchemyListingRepository(ListingRepositoryPort):
    def __init__(self, database: DatabaseConnection) -> None: self.database = database
    def get(self, listing_id: str) -> Listing | None:
        with self.database.engine.connect() as connection:
            row = connection.execute(text("SELECT listing_id,security_id FROM listings WHERE listing_id=:id"), {"id": listing_id}).mappings().first()
        return Listing(str(row["listing_id"]), str(row["security_id"])) if row else None
    def save(self, listing: Listing) -> None:
        try:
            with self.database.engine.begin() as connection:
                connection.execute(text("INSERT INTO listings(listing_id,security_id) VALUES(:id,:security_id) ON CONFLICT(listing_id) DO UPDATE SET security_id=EXCLUDED.security_id"), {"id":listing.listing_id,"security_id":listing.security_id})
        except IntegrityError as exc:
            raise PersistenceError("Unable to persist listing", PersistenceFailureKind.INTEGRITY_VIOLATION) from exc

class SqlAlchemyIdentifierMappingRepository(IdentifierMappingRepositoryPort):
    def __init__(self, database: DatabaseConnection) -> None: self.database = database
    def find(self, provider_id: str, external_identifier: str) -> IdentifierMapping | None:
        with self.database.engine.connect() as connection:
            row=connection.execute(text("SELECT provider_id,external_identifier,canonical_identifier FROM identifier_mappings WHERE provider_id=:p AND external_identifier=:e"),{"p":provider_id,"e":external_identifier}).mappings().first()
        return IdentifierMapping(str(row["provider_id"]),str(row["external_identifier"]),str(row["canonical_identifier"])) if row else None
    def save(self, mapping: IdentifierMapping) -> None:
        with self.database.engine.begin() as connection:
            connection.execute(text("INSERT INTO identifier_mappings(provider_id,external_identifier,canonical_identifier) VALUES(:p,:e,:c) ON CONFLICT(provider_id,external_identifier) DO UPDATE SET canonical_identifier=EXCLUDED.canonical_identifier"),{"p":mapping.provider_id,"e":mapping.external_identifier,"c":mapping.canonical_identifier})

class SqlAlchemyMarketObservationRepository(MarketObservationRepositoryPort):
    def __init__(self, database: DatabaseConnection) -> None: self.database=database
    @staticmethod
    def _to_domain(row: object) -> MarketObservation:
        r=row
        return MarketObservation(str(r["listing_id"]),r["observed_at"],r["available_at"],Decimal(str(r["open"])) if r["open"] is not None else None,Decimal(str(r["high"])) if r["high"] is not None else None,Decimal(str(r["low"])) if r["low"] is not None else None,Decimal(str(r["close"])),Decimal(str(r["volume"])) if r["volume"] is not None else None,str(r["currency"]),str(r["frequency"]),bool(r["adjusted"]),SourceIdentity(str(r["provider_id"]),str(r["source_record_id"])))
    def save(self, observation: MarketObservation) -> None:
        try:
            with self.database.engine.begin() as connection:
                connection.execute(text("INSERT INTO market_observations(listing_id,observed_at,available_at,open,high,low,close,volume,currency,frequency,adjusted,provider_id,source_record_id) VALUES(:l,:o,:a,:op,:h,:lo,:c,:v,:cu,:f,:ad,:p,:s) ON CONFLICT DO NOTHING"),{"l":observation.listing_id,"o":observation.observed_at,"a":observation.available_at,"op":observation.open,"h":observation.high,"lo":observation.low,"c":observation.close,"v":observation.volume,"cu":observation.currency,"f":observation.frequency,"ad":observation.adjusted,"p":observation.source_identity.provider_id,"s":observation.source_identity.source_record_id})
        except IntegrityError as exc:
            raise PersistenceError("Unable to persist market observation",PersistenceFailureKind.INTEGRITY_VIOLATION) from exc
    def find_existing(self, observation: MarketObservation) -> MarketObservation | None:
        with self.database.engine.connect() as connection:
            row=connection.execute(text("SELECT * FROM market_observations WHERE listing_id=:l AND observed_at=:o AND frequency=:f AND adjusted=:a AND provider_id=:p AND source_record_id=:s"),{"l":observation.listing_id,"o":observation.observed_at,"f":observation.frequency,"a":observation.adjusted,"p":observation.source_identity.provider_id,"s":observation.source_identity.source_record_id}).mappings().first()
        return self._to_domain(row) if row else None
    def get_by_listing_and_period(self, listing_id: str, start: datetime, end: datetime) -> tuple[MarketObservation,...]:
        with self.database.engine.connect() as connection:
            rows=connection.execute(text("SELECT * FROM market_observations WHERE listing_id=:l AND observed_at>=:s AND observed_at<:e ORDER BY observed_at"),{"l":listing_id,"s":start,"e":end}).mappings().all()
        return tuple(self._to_domain(r) for r in rows)
    def get_as_of(self, listing_id: str, observed_at: datetime, available_at: datetime) -> tuple[MarketObservation,...]:
        with self.database.engine.connect() as connection:
            rows=connection.execute(text("SELECT * FROM market_observations WHERE listing_id=:l AND observed_at<=:o AND (available_at IS NULL OR available_at<=:a) ORDER BY observed_at"),{"l":listing_id,"o":observed_at,"a":available_at}).mappings().all()
        return tuple(self._to_domain(r) for r in rows)

class SqlAlchemyCorporateActionRepository(CorporateActionRepositoryPort):
    def __init__(self,database:DatabaseConnection)->None:self.database=database
    def save(self,action:CorporateAction)->None:
        with self.database.engine.begin() as connection:
            connection.execute(text("INSERT INTO corporate_actions(action_id,listing_id,effective_at,action_type) VALUES(:i,:l,:e,:t) ON CONFLICT(action_id) DO NOTHING"),{"i":action.action_id,"l":action.listing_id,"e":action.effective_at,"t":action.action_type})
    def get_by_listing_and_period(self,listing_id:str,start:datetime,end:datetime)->tuple[CorporateAction,...]:
        with self.database.engine.connect() as connection:
            rows=connection.execute(text("SELECT action_id,listing_id,effective_at,action_type FROM corporate_actions WHERE listing_id=:l AND effective_at>=:s AND effective_at<:e ORDER BY effective_at"),{"l":listing_id,"s":start,"e":end}).mappings().all()
        return tuple(CorporateAction(str(r["action_id"]),str(r["listing_id"]),r["effective_at"],str(r["action_type"])) for r in rows)

class SqlAlchemySourceRecordRepository(SourceRecordRepositoryPort):
    def __init__(self,database:DatabaseConnection)->None:self.database=database
    def save(self,record:SourceRecord)->None:
        with self.database.engine.begin() as connection:
            connection.execute(text("INSERT INTO source_records(provider_id,source_record_id,adapter_id,request_id,retrieved_at,artifact_reference,content_hash,content_type,validation_state) VALUES(:p,:s,:a,:r,:t,:ar,:h,:c,:v) ON CONFLICT(provider_id,source_record_id) DO NOTHING"),{"p":record.source_identity.provider_id,"s":record.source_identity.source_record_id,"a":record.adapter_id,"r":record.request_id,"t":record.retrieved_at,"ar":record.artifact_reference,"h":record.content_hash,"c":record.content_type,"v":str(record.validation_state)})
    def find_by_source_identity(self,identity:SourceIdentity)->SourceRecord|None:
        with self.database.engine.connect() as connection:
            row=connection.execute(text("SELECT * FROM source_records WHERE provider_id=:p AND source_record_id=:s"),{"p":identity.provider_id,"s":identity.source_record_id}).mappings().first()
        return SourceRecord(str(row["adapter_id"]),SourceIdentity(str(row["provider_id"]),str(row["source_record_id"])),str(row["request_id"]),row["retrieved_at"],str(row["artifact_reference"]),str(row["content_hash"]),str(row["content_type"]),row["validation_state"]) if row else None

class SqlAlchemyProvenanceRepository(ProvenanceRepositoryPort):
    def __init__(self,database:DatabaseConnection)->None:self.database=database
    def save(self,provenance:Provenance)->None:
        with self.database.engine.begin() as connection:
            connection.execute(text("INSERT INTO provenance(provenance_id,source_record_id,transformation_version) VALUES(:i,:s,:v) ON CONFLICT(provenance_id) DO UPDATE SET source_record_id=EXCLUDED.source_record_id,transformation_version=EXCLUDED.transformation_version"),{"i":provenance.provenance_id,"s":provenance.source_record_id,"v":provenance.transformation_version})
    def get(self,provenance_id:str)->Provenance|None:
        with self.database.engine.connect() as connection:
            row=connection.execute(text("SELECT provenance_id,source_record_id,transformation_version FROM provenance WHERE provenance_id=:i"),{"i":provenance_id}).mappings().first()
        return Provenance(str(row["provenance_id"]),str(row["source_record_id"]),str(row["transformation_version"])) if row else None
