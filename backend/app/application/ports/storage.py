"""Provider-neutral raw-artifact storage port."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceArtifactReference:
    artifact_id: str
    content_hash: str
    content_type: str
    size_bytes: int
    object_reference: str


@dataclass(frozen=True)
class RawPayload:
    content: bytes
    content_type: str
    content_hash: str


class RawArtifactStore(Protocol):
    def store(
        self,
        payload: bytes,
        *,
        content_type: str,
        artifact_id: str,
    ) -> SourceArtifactReference:
        ...

    def retrieve(
        self,
        reference: SourceArtifactReference,
    ) -> RawPayload:
        ...

    def exists(
        self,
        reference: SourceArtifactReference,
    ) -> bool:
        ...
