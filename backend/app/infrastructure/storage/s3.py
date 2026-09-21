"""S3-compatible raw artifact adapter."""
from hashlib import sha256
import boto3
from botocore.client import Config
from app.application.ports.storage import RawArtifactStore, RawPayload, SourceArtifactReference
from app.config import Settings
class S3RawArtifactStore(RawArtifactStore):
    def __init__(self, settings: Settings) -> None:
        if settings.raw_storage_endpoint is None:
            raise RuntimeError("RAW_STORAGE_ENDPOINT is required for object storage")
        self._bucket = settings.raw_storage_bucket
        self._client = boto3.client(
            "s3", endpoint_url=settings.raw_storage_endpoint, region_name=settings.raw_storage_region,
            aws_access_key_id=settings.raw_storage_access_key, aws_secret_access_key=settings.raw_storage_secret_key,
            use_ssl=settings.raw_storage_secure, config=Config(s3={"addressing_style": "path"}),
        )
        self._ensure_bucket()
    def _ensure_bucket(self) -> None:
        buckets = self._client.list_buckets().get("Buckets", [])
        if not any(item["Name"] == self._bucket for item in buckets):
            self._client.create_bucket(Bucket=self._bucket)
    def store(self, payload: bytes, *, content_type: str, artifact_id: str) -> SourceArtifactReference:
        digest = sha256(payload).hexdigest()
        try:
            existing = self._client.head_object(Bucket=self._bucket, Key=artifact_id)
            if existing.get("Metadata", {}).get("content-sha256") != digest:
                raise ValueError(f"artifact_id {artifact_id} already contains different content")
        except self._client.exceptions.ClientError as exc:
            if exc.response.get("Error", {}).get("Code") not in {"404", "NoSuchKey"}:
                raise
            self._client.put_object(
                Bucket=self._bucket, Key=artifact_id, Body=payload, ContentType=content_type,
                Metadata={"content-sha256": digest},
            )
        return SourceArtifactReference(artifact_id, digest, content_type, len(payload), f"s3://{self._bucket}/{artifact_id}")
    def retrieve(self, reference: SourceArtifactReference) -> RawPayload:
        response = self._client.get_object(Bucket=self._bucket, Key=reference.artifact_id)
        content = response["Body"].read()
        digest = sha256(content).hexdigest()
        if digest != reference.content_hash:
            raise ValueError("raw artifact content hash mismatch")
        return RawPayload(content, reference.content_type, digest)
    def exists(self, reference: SourceArtifactReference) -> bool:
        try:
            self._client.head_object(Bucket=self._bucket, Key=reference.artifact_id)
            return True
        except self._client.exceptions.ClientError as exc:
            if exc.response.get("Error", {}).get("Code") in {"404", "NoSuchKey"}:
                return False
            raise
