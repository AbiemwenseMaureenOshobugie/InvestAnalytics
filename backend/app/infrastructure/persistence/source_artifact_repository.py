"""Source-artifact metadata repository adapter."""
from app.application.ports.repositories import SourceArtifactRepositoryPort
from app.application.ports.storage import SourceArtifactMetadata
from app.infrastructure.persistence.database import DatabaseConnection
from sqlalchemy import text
class SqlAlchemySourceArtifactRepository(SourceArtifactRepositoryPort):
    def __init__(self, database: DatabaseConnection) -> None:
        self.database = database
    def save(self, artifact: SourceArtifactMetadata) -> None:
        with self.database.engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO source_artifacts "
                    "(artifact_id, provider_id, retrieved_at, content_hash, content_type, size_bytes, "
                    "object_reference, ingestion_status, validation_state) "
                    "VALUES (:i,:p,:r,:h,:c,:s,:o,:is,:v) "
                    "ON CONFLICT (artifact_id) DO UPDATE SET "
                    "content_hash=EXCLUDED.content_hash, size_bytes=EXCLUDED.size_bytes, "
                    "object_reference=EXCLUDED.object_reference, validation_state=EXCLUDED.validation_state"
                ),
                {
                    "i": artifact.artifact_id, "p": artifact.provider_id, "r": artifact.retrieved_at,
                    "h": artifact.content_hash, "c": artifact.content_type, "s": artifact.size_bytes,
                    "o": artifact.object_reference, "is": artifact.ingestion_status,
                    "v": artifact.validation_state,
                },
            )
    def get(self, artifact_id: str) -> SourceArtifactMetadata | None:
        with self.database.engine.connect() as connection:
            row = connection.execute(
                text("SELECT * FROM source_artifacts WHERE artifact_id=:id"), {"id": artifact_id}
            ).mappings().first()
        if row is None:
            return None
        return SourceArtifactMetadata(
            artifact_id=str(row["artifact_id"]), provider_id=str(row["provider_id"]),
            retrieved_at=row["retrieved_at"], content_hash=str(row["content_hash"]),
            content_type=str(row["content_type"]), size_bytes=int(row["size_bytes"]),
            object_reference=str(row["object_reference"]), ingestion_status=str(row["ingestion_status"]),
            validation_state=str(row["validation_state"]),
        )
