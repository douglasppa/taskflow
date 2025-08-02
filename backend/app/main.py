from fastapi import FastAPI
from contextlib import asynccontextmanager

from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.init_db import run_migrations
from app.core.logger import log, LogLevel

from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_monitoring import router as monitoring_router
from app.api.v1.routes_metrics import router as metrics_router
from app.services.metrics import update_frontend_metrics

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
    "https://taskflow-frontend-ylgl.onrender.com",  # Frontend em produção
    "https://taskflow-frontend-roan.vercel.app",  # Frontend em produção
    "https://frontend-five-rho-11.vercel.app",  # Frontend em produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] em dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def update_metrics_before_request(request, call_next):
    if request.url.path == "/metrics":
        update_frontend_metrics()
    response = await call_next(request)
    return response


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
app.include_router(metrics_router, prefix=settings.API_V1_STR)
