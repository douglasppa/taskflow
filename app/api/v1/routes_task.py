from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task as task_service
from app.db.session import get_db
from app.auth.auth_bearer import JWTBearer
from http import HTTPStatus
import asyncio
from app.core.logger import log

router = APIRouter(
    prefix="/tasks", tags=["Task Management"], dependencies=[Depends(JWTBearer())]
)


@router.post(
    "/",
    response_model=TaskOut,
    summary="Create a new task",
    status_code=HTTPStatus.CREATED,
)
async def create_task(
    task: TaskCreate, db: Session = Depends(get_db), user=Depends(JWTBearer())
):
    log("Received request to create a new task", level="INFO")
    log(
        f"Flag simulate_task_latency: {settings.features.simulate_task_latency}",
        level="DEBUG",
    )
    if settings.features.simulate_task_latency:
        await asyncio.sleep(3)  # delay artificial para testes
    db_task = task_service.create_task(db, task, user)
    return db_task


@router.get(
    "/summary",
    summary="List task summary for the authenticated user",
    status_code=HTTPStatus.OK,
)
async def task_summary(db: Session = Depends(get_db), user=Depends(JWTBearer())):
    log(f"Generating task summary for user ID: {user['sub']}", level="DEBUG")
    log(
        f"Flag enable_summary_endpoint: {settings.features.enable_summary_endpoint}",
        level="DEBUG",
    )

    if not settings.features.enable_summary_endpoint:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Endpoint not available"
        )

    try:
        count = (
            db.query(func.count(Task.id))
            .filter(Task.owner_id == int(user["sub"]))
            .scalar()
        )

        return {
            "user_id": int(user["sub"]),
            "total_tasks": count,
        }

    except Exception:
        log("Error generating task summary", level="ERROR")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to generate task summary",
        )


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    summary="Get a task by ID",
    status_code=HTTPStatus.OK,
)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        log(f"Task not found with ID: {task_id}", level="ERROR")
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value, detail="Task not found"
        )
    return db_task


@router.get(
    "/",
    response_model=list[TaskOut],
    summary="List all tasks",
    status_code=HTTPStatus.OK,
)
async def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    summary="Update a task by ID",
    status_code=HTTPStatus.OK,
)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(JWTBearer()),
):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        log(f"Task not found with ID: {task_id}", level="ERROR")
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value, detail="Task not found"
        )
    if db_task.owner_id != int(user["sub"]):
        log(
            f"User {user['sub']} not authorized to update task with ID: {task_id}",
            level="WARNING",
        )

        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN.value,
            detail="Not authorized to update this task",
        )

    updated = task_service.update_task(db, task_id, task, user)
    return updated


@router.delete(
    "/{task_id}", summary="Delete a task by ID", status_code=HTTPStatus.NO_CONTENT
)
async def delete_task(
    task_id: int, db: Session = Depends(get_db), user=Depends(JWTBearer())
):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        log(f"Task not found with ID: {task_id}", level="ERROR")
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value, detail="Task not found"
        )
    if db_task.owner_id != int(user["sub"]):
        log(
            f"User {user['sub']} not authorized to delete task with ID: {task_id}",
            level="WARNING",
        )
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN.value,
            detail="Not authorized to delete this task",
        )

    deleted = task_service.delete_task(db, task_id, user)
    if not deleted:
        log(f"Failed to delete task with ID {task_id}", level="ERROR")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Failed to delete task",
        )
    log(f"Task with ID {task_id} deleted successfully", level="INFO")
    return {"message": "Task deleted"}
