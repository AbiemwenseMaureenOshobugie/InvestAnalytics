from pathlib import Path

ROOT = Path(__file__).parents[1] / "app"


def test_domain_does_not_import_frameworks_or_infrastructure() -> None:
    for path in (ROOT / "domain").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "fastapi" not in text.lower()
        assert "infrastructure" not in text.lower()


def test_application_does_not_import_provider_sdks() -> None:
    for path in (ROOT / "application").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "provider" not in text.lower()
        assert "sdk" not in text.lower()
