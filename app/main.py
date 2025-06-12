from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.api.v1.routes_task import router as task_router
from app.api.v1.routes_auth import router as auth_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="TaskFlow")

Instrumentator().instrument(app).expose(app)

app.include_router(api_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")