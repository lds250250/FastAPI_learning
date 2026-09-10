from fastapi import FastAPI
from my_fastapi_project.core.config import get_settings
from my_fastapi_project.api.routers.user import router as user_router
from my_fastapi_project.api.routers.health import router as health_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
app.include_router(user_router)
app.include_router(health_router)
