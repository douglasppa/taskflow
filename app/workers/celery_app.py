from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend="rpc://"
)

celery_app.autodiscover_tasks(["app.workers.logging_tasks"])