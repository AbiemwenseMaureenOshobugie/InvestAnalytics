import ast
from pathlib import Path

ROOT = Path(__file__).parents[1] / "app"


DISALLOWED_MODULES = frozenset({
    "httpx",
    "requests",
    "aiohttp",
    "kobo",
    "eodhd",
    "boto3",
    "minio",
    "sqlalchemy",
    "psycopg",
    "asyncpg",
})


def _has_disallowed_import(path: Path) -> tuple[str, int] | None:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in DISALLOWED_MODULES:
                    return alias.name, node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in DISALLOWED_MODULES:
                return node.module, node.lineno
    return None


def test_domain_does_not_import_frameworks_or_infrastructure() -> None:
    for path in (ROOT / "domain").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "fastapi" not in text.lower()
        assert "infrastructure" not in text.lower()


def test_application_does_not_import_provider_sdks() -> None:
    for path in (ROOT / "application").rglob("*.py"):
        result = _has_disallowed_import(path)
        if result is not None:
            module, line = result
            raise AssertionError(
                f"{path} imports disallowed module '{module}' at line {line}"
            )


def test_application_does_not_import_sdk_directly() -> None:
    for path in (ROOT / "application").rglob("*.py"):
        result = _has_disallowed_import(path)
        if result is not None and "sdk" in result[0].lower():
            module, line = result
            raise AssertionError(
                f"{path} imports SDK module '{module}' at line {line}"
            )
