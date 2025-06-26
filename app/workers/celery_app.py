from celery import Celery
from app.core.config import settings


celery_app = Celery("worker", broker=settings.RABBITMQ_URL, backend="rpc://")

celery_app.autodiscover_tasks(["app.workers.logging_tasks"])
