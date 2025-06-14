from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    owner_id: int  # para simplificar, sem autenticação por enquanto

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)