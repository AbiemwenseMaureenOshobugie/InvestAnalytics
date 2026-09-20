from typing import Protocol

from app.config import Settings


class DatabaseHealth(Protocol):
    def check(self) -> bool: ...


class DatabaseConnection:
    """IA-0A database boundary; no domain persistence is implemented yet."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def check(self) -> bool:
        # PostgreSQL connectivity is deliberately deferred in IA-0A.
        return self._settings.database_url is None

    @property
    def configured(self) -> bool:
        return self._settings.database_url is not None
