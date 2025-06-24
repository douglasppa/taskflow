from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
import pika
import os
from pymongo import MongoClient
import logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Monitoring"])

@router.get("/health/live", summary="Liveness probe")
def liveness_probe():
    return {"status": "alive"}

@router.get("/health/ready", summary="Readiness probe")
def readiness_probe(db: Session = Depends(get_db)):
    errors = []

    # PostgreSQL
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        errors.append(f"PostgreSQL: {e}")

    # MongoDB
    try:
        mongo_url = os.getenv("MONGO_URL", "mongodb://mongo_db:27017")
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=500)
        client.server_info()
        client.close()
        logger.info("MongoDB connection successful")
    except Exception as e:
        errors.append(f"MongoDB: {e}")

    # RabbitMQ
    try:
        rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672")
        connection = pika.BlockingConnection(pika.URLParameters(rabbit_url))
        connection.close()
        logger.info("RabbitMQ connection successful")
    except Exception as e:
        logger.exception("Failed to connect to RabbitMQ")
        errors.append(f"RabbitMQ: {type(e).__name__} - {str(e) or repr(e)}")

    if errors:
        return {"status": "degraded", "errors": errors}
    
    return {"status": "ready"}