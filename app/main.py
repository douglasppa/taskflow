from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.init_db import run_migrations

from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_monitoring import router as monitoring_router

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

Instrumentator().instrument(app).expose(app)

# Include routers for different API versions and functionalities
app.include_router(task_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(monitoring_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Run migrations on startup."""
    run_migrations()