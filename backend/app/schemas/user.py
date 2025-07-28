from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Payload de entrada no endpoint POST /auth/register"""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Payload de entrada no endpoint POST /auth/login"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Resposta dos endpoints GET /auth/user e POST /auth/login"""

    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class ForgotPasswordRequest(BaseModel):
    """Payload de entrada no endpoint POST /auth/forgot-password"""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Payload de entrada no endpoint POST /auth/reset-password"""

    token: str
    new_password: str
