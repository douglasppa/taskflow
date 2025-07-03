from app.workers.celery_app import celery_app
from app.services.logger import log_event as sync_log_event
from app.core.logger import log, LogLevel


@celery_app.task(name="app.workers.logging_tasks.test_task")
def test_task():
    log("Celery está funcionando!", level=LogLevel.INFO)
    return "Hello from Celery"


@celery_app.task(name="app.workers.logging_tasks.log_event")
def log_event(user_id: str, action: str, data: dict):
    sync_log_event(user_id=user_id, action=action, data=data)
