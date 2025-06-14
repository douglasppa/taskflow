from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings

from app.api.v1.routes import router as api_router
from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router

app = FastAPI(title=settings.PROJECT_NAME)

Instrumentator().instrument(app).expose(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(task_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)