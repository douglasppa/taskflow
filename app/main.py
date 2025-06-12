from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.api.v1.routes_task import router as task_router

app = FastAPI(title="TaskFlow")

app.include_router(api_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")