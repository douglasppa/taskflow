from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db
import pika
from pymongo import MongoClient
from app.core.logger import log, LogLevel

router = APIRouter(tags=["Monitoring"])


@router.get("/health/live", summary="Liveness probe")
def liveness_probe():
    log("Liveness probe called", level=LogLevel.INFO)
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness probe")
def readiness_probe(db: Session = Depends(get_db)):
    log("Readiness probe called", level=LogLevel.INFO)
    errors = []

    # PostgreSQL
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        errors.append(f"PostgreSQL: {e}")

    # MongoDB
    try:
        client = MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=500)
        client.server_info()
        client.close()
        log("MongoDB connection successful", level=LogLevel.INFO)
    except Exception as e:
        errors.append(f"MongoDB: {e}")

    # RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        connection.close()
        log("RabbitMQ connection successful", level=LogLevel.INFO)
    except Exception as e:
        log("Failed to connect to RabbitMQ", level=LogLevel.ERROR)
        errors.append(f"RabbitMQ: {type(e).__name__} - {str(e) or repr(e)}")

    if errors:
        return {"status": "degraded", "errors": errors}

    return {"status": "ready"}


@router.get("/info", summary="Application Info")
def app_info():
    log("Fetching application info", level=LogLevel.INFO)
    try:
        features = settings.features.model_dump(mode="json")
    except Exception as e:
        log("Erro ao acessar settings.features", level=LogLevel.ERROR)
        features = {"error": str(e)}

    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "feature_flags": features,
    }
