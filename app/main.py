from fastapi import FastAPI
from contextlib import asynccontextmanager

from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.init_db import run_migrations
from app.core.logger import log, LogLevel

from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_monitoring import router as monitoring_router

import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

log("FastAPI is starting!", level=LogLevel.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executado na inicialização da aplicação."""
    run_migrations()
    yield
    # Aqui poderia entrar algum shutdown future (como fechar conexões)


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.include_router(task_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(monitoring_router, prefix=settings.API_V1_STR)
