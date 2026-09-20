from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.infrastructure.persistence.database import DatabaseConnection

router = APIRouter()


@router.get("/health", tags=["infrastructure"])
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name}


@router.get("/readiness", tags=["infrastructure"])
def readiness() -> JSONResponse:
    settings = get_settings()
    database = DatabaseConnection(settings)

    if not database.configured:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "dependency": "database", "reason": "not_configured"},
        )

    if not database.check():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "dependency": "database", "reason": "unavailable"},
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ready"})
