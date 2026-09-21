from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
Environment = Literal["development", "test", "staging", "production"]
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)
    app_name: str = "InvestAnalytics"
    app_version: str = "0.1.0"
    environment: Environment = "development"
    api_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    database_url: str | None = None
    log_level: str = "INFO"
    allowed_origins: list[str] = ["http://localhost:5173"]
    raw_storage_endpoint: str | None = None
    raw_storage_bucket: str = "investanalytics-raw"
    raw_storage_region: str = "us-east-1"
    raw_storage_access_key: str | None = None
    raw_storage_secret_key: str | None = None
    raw_storage_secure: bool = False
@lru_cache
def get_settings() -> Settings:
    return Settings()
