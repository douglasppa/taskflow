from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str

class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

model_config = {
    "from_attributes": True
}