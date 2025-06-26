from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings
from app.core.init_db import run_migrations
from app.core.logger import log

from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_monitoring import router as monitoring_router

import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

log("FastAPI is starting!", level="INFO")

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
