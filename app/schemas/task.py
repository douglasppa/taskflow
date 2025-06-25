"""
Schemas relacionados à entidade Task.

Usados em:
- API REST (rota /tasks) para criação, atualização e listagem de tarefas.
- Envio de logs para Celery (task_created, task_updated, etc.)
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    # Base para os schemas de Task
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    # Usado como payload de entrada no endpoint POST /tasks
    pass


class TaskUpdate(TaskBase):
    # Usado como payload de entrada no endpoint PUT /tasks/{id}
    pass


class TaskOut(TaskBase):
    # Usado como resposta nos endpoints GET /tasks e GET /tasks/{id}
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
