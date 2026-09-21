# ruff: noqa: E501
"""IA-1C persistence foundation."""
import sqlalchemy as sa
from alembic import op


revision = "0001_ia1c_persistence_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("data_sources",
        sa.Column("source_id", sa.String(100), primary_key=True),
        sa.Column("provider_id", sa.String(100), nullable=False, unique=True),
        sa.Column("provider_name", sa.String(200), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_table("securities", sa.Column("security_id", sa.String(100), primary_key=True))
    op.create_table("listings",
        sa.Column("listing_id", sa.String(100), primary_key=True),
        sa.Column("security_id", sa.String(100), sa.ForeignKey("securities.security_id"), nullable=False))
    op.create_table("identifier_mappings",
        sa.Column("provider_id", sa.String(100), nullable=False),
        sa.Column("external_identifier", sa.String(200), nullable=False),
        sa.Column("canonical_identifier", sa.String(200), nullable=False),
        sa.PrimaryKeyConstraint("provider_id", "external_identifier"))
    op.create_table("source_artifacts",
        sa.Column("artifact_id", sa.String(200), primary_key=True),
        sa.Column("provider_id", sa.String(100), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("content_type", sa.String(200), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("object_reference", sa.String(1000), nullable=False, unique=True),
        sa.Column("ingestion_status", sa.String(50), nullable=False),
        sa.Column("validation_state", sa.String(50), nullable=False))
    op.create_table("source_records",
        sa.Column("provider_id", sa.String(100), nullable=False),
        sa.Column("source_record_id", sa.String(200), nullable=False),
        sa.Column("adapter_id", sa.String(100), nullable=False),
        sa.Column("request_id", sa.String(200), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("artifact_reference", sa.String(200), sa.ForeignKey("source_artifacts.artifact_id"), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("content_type", sa.String(200), nullable=False),
        sa.Column("validation_state", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("provider_id", "source_record_id"))
    op.create_table("provenance",
        sa.Column("provenance_id", sa.String(100), primary_key=True),
        sa.Column("source_record_id", sa.String(200), nullable=False),
        sa.Column("transformation_version", sa.String(100), nullable=False))
    op.create_table("market_observations",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("listing_id", sa.String(100), sa.ForeignKey("listings.listing_id"), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True)),
        sa.Column("open", sa.Numeric(30, 10)),
        sa.Column("high", sa.Numeric(30, 10)),
        sa.Column("low", sa.Numeric(30, 10)),
        sa.Column("close", sa.Numeric(30, 10), nullable=False),
        sa.Column("volume", sa.Numeric(30, 10)),
        sa.Column("currency", sa.String(20), nullable=False),
        sa.Column("frequency", sa.String(30), nullable=False),
        sa.Column("adjusted", sa.Boolean(), nullable=False),
        sa.Column("provider_id", sa.String(100), nullable=False),
        sa.Column("source_record_id", sa.String(200), nullable=False),
        sa.ForeignKeyConstraint(["provider_id", "source_record_id"], ["source_records.provider_id", "source_records.source_record_id"]),
        sa.UniqueConstraint("listing_id", "observed_at", "frequency", "adjusted", "provider_id", "source_record_id",
                            name="uq_market_observation_identity"))
    op.create_index("ix_market_observations_listing_observed", "market_observations", ["listing_id", "observed_at"])
    op.create_index("ix_market_observations_listing_available", "market_observations", ["listing_id", "available_at"])
    op.create_table("corporate_actions",
        sa.Column("action_id", sa.String(100), primary_key=True),
        sa.Column("listing_id", sa.String(100), sa.ForeignKey("listings.listing_id"), nullable=False),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("action_type", sa.String(50), nullable=False))
def downgrade() -> None:
    op.drop_table("corporate_actions")
    op.drop_index("ix_market_observations_listing_available", table_name="market_observations")
    op.drop_index("ix_market_observations_listing_observed", table_name="market_observations")
    op.drop_table("market_observations")
    op.drop_table("provenance")
    op.drop_table("source_records")
    op.drop_table("source_artifacts")
    op.drop_table("identifier_mappings")
    op.drop_table("listings")
    op.drop_table("securities")
    op.drop_table("data_sources")
