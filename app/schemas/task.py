from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Usado como payload de entrada no endpoint POST /tasks"""

    pass


class TaskUpdate(BaseModel):
    """Usado como payload de entrada no endpoint PUT /tasks/{id}"""

    title: Optional[str] = None
    description: Optional[str] = None


class TaskOut(TaskBase):
    """Usado como resposta nos endpoints GET /tasks e GET /tasks/{id}"""

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
