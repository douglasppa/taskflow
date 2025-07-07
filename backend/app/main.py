from fastapi import FastAPI
from contextlib import asynccontextmanager

from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.init_db import run_migrations
from app.core.logger import log, LogLevel

from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_monitoring import router as monitoring_router

from fastapi.middleware.cors import CORSMiddleware
import sys

# Reconfigure stdout and stderr for line buffering
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

log("FastAPI is starting!", level=LogLevel.INFO)


# Async initialization for migrations
@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


# Application instance
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Enable CORS middleware
origins = [
    "http://localhost:5173",  # Vite local
    "http://127.0.0.1:5173",  # Alternativo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] em dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus instrumentation
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    excluded_handlers=["/metrics", "/health/live", "/health/ready"],
).instrument(app).expose(app)

# API routers
app.include_router(task_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(monitoring_router, prefix=settings.API_V1_STR)
