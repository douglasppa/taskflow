from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task as task_service
from app.db.session import SessionLocal
from app.db.session import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(JWTBearer())])

@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, db: Session = Depends(get_db), user = Depends(JWTBearer())):
    db_task = task_service.create_task(db, task, user)
    return db_task

@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/", response_model=list[TaskOut])
async def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), user = Depends(JWTBearer())):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    updated = task_service.update_task(db, task_id, task, user)
    return updated

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), user = Depends(JWTBearer())):
    db_task = task_service.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != int(user["sub"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    deleted = task_service.delete_task(db, task_id, user)
    return {"message": "Task deleted"}