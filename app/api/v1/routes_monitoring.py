from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.session import get_db
import pika
import os
from pymongo import MongoClient
from app.core.logger import log

router = APIRouter(tags=["Monitoring"])


@router.get("/health/live", summary="Liveness probe")
def liveness_probe():
    log("Liveness probe called", level="INFO")
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness probe")
def readiness_probe(db: Session = Depends(get_db)):
    log("Readiness probe called", level="INFO")
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
        log("MongoDB connection successful", level="INFO")
    except Exception as e:
        errors.append(f"MongoDB: {e}")

    # RabbitMQ
    try:
        rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672")
        connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
        connection.close()
        log("RabbitMQ connection successful", level="INFO")
    except Exception as e:
        log("Failed to connect to RabbitMQ", level="ERROR")
        errors.append(f"RabbitMQ: {type(e).__name__} - {str(e) or repr(e)}")

    if errors:
        return {"status": "degraded", "errors": errors}

    return {"status": "ready"}


@router.get("/info", summary="Application Info")
def app_info():
    log("Fetching application info", level="INFO")
    try:
        features = settings.features.dict()
    except Exception as e:
        log("Erro ao acessar settings.features", level="ERROR")
        features = {"error": str(e)}

    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "feature_flags": features,
    }
