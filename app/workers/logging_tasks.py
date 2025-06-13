from app.workers.celery_app import celery_app
from app.services.logger_service import log_event as sync_log_event

@celery_app.task(name="app.workers.logging_tasks.test_task")
def test_task():
    print("🚀 Celery está funcionando!")
    return "Hello from Celery"

@celery_app.task(name="app.workers.logging_tasks.log_event")
def log_event(user_id: str, action: str, data: dict):
    sync_log_event(user_id=user_id, action=action, data=data)