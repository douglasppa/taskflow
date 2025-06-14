"""
Schemas relacionados à entidade User.

Usados em:
- API REST (rota /auth) para registro, login e resposta de autenticação.
"""

from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    # Usado como payload de entrada no endpoint POST /auth/register
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    # Usado como payload de entrada no endpoint POST /auth/login
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    # Usado como resposta nos endpoints GET /auth/user e POST /auth/login
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)