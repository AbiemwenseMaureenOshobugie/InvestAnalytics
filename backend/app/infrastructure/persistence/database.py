# ruff: noqa: E501
"""PostgreSQL persistence boundary for IA-1C."""
from collections.abc import Generator
from typing import Protocol

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings


class DatabaseHealth(Protocol):
    def check(self) -> bool: ...
class DatabaseConnection:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None
    def _get_engine(self) -> Engine:
        if self._settings.database_url is None:
            raise RuntimeError("DATABASE_URL is required for PostgreSQL persistence")
        if self._engine is None:
            self._engine = create_engine(self._settings.database_url, pool_pre_ping=True, future=True)
            self._session_factory = sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)
        return self._engine
    def check(self) -> bool:
        if self._settings.database_url is None:
            return False
        try:
            with self._get_engine().connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
    @property
    def configured(self) -> bool:
        return self._settings.database_url is not None
    @property
    def engine(self) -> Engine:
        return self._get_engine()
    def session(self) -> Generator[Session, None, None]:
        if self._session_factory is None:
            self._get_engine()
        assert self._session_factory is not None
        with self._session_factory() as session:
            yield session
