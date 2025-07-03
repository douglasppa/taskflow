from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.workers.logging_tasks import log_event
from app.models.user import User
from app.constants.actions import LogAction, LOG_SEND_MSG
from app.core.metrics import task_created_total
from app.core.logger import log, LogLevel


def create_task(db: Session, task_data: TaskCreate, user: User):
    db_task = Task(**task_data.model_dump(), owner_id=str(user["sub"]))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    task_created_total.inc()
    log(f"Task created: {db_task.id} by user {user['sub']}", level=LogLevel.INFO)
    try:
        log_event.delay(
            str(user["sub"]),
            LogAction.TASK_CREATE,
            {"task_id": db_task.id, "title": db_task.title},
        )
        log(LOG_SEND_MSG, level=LogLevel.INFO)
    except Exception as e:
        log(f"Erro ao enviar log async: {e}", level=LogLevel.ERROR)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).offset(skip).limit(limit).all()


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user: User):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
        log(f"Task updated: {db_task.id} by user {user['sub']}", level=LogLevel.INFO)
        try:
            log_event.delay(
                str(user["sub"]),
                LogAction.TASK_UPDATE,
                {"task_id": db_task.id, "title": db_task.title},
            )
            log(LOG_SEND_MSG, level=LogLevel.INFO)
        except Exception as e:
            log(f"Erro ao enviar log async: {e}", level=LogLevel.ERROR)
    return db_task


def delete_task(db: Session, task_id: int, user: User):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        log(f"Task deleted: {db_task.id} by user {user['sub']}", level=LogLevel.INFO)
        try:
            log_event.delay(
                str(user["sub"]),
                LogAction.TASK_DELETE,
                {"task_id": db_task.id, "title": db_task.title},
            )
            log(LOG_SEND_MSG, level=LogLevel.INFO)
        except Exception as e:
            log(f"Erro ao enviar log async: {e}", level=LogLevel.ERROR)
    return db_task
