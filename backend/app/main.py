from fastapi import FastAPI

from app.config import get_settings
from app.interfaces.api.routes import router


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, version=settings.app_version)
    application.include_router(router, prefix=settings.api_prefix)
    return application


app = create_app()
