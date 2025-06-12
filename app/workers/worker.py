from celery import Celery

celery_app = Celery(
    "taskflow",
    broker="amqp://guest:guest@rabbitmq:5672//",
)

@celery_app.task
def test_task():
    print("🚀 Celery está funcionando!")
    return "Hello from Celery"