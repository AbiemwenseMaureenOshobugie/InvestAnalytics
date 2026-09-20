import pytest
from pydantic import ValidationError

from app.config import Settings


def test_settings_defaults_are_valid() -> None:
    settings = Settings()
    assert settings.app_name == "InvestAnalytics"
    assert settings.port == 8000


def test_invalid_port_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(port=0)
