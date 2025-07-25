from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.constants.actions import LogAction
from app.auth.auth_handler import create_access_token
from app.workers.logging_tasks import log_event
from app.core.metrics import user_login_total
from app.core.config import settings
from app.constants.actions import LOG_SEND_MSG
from fastapi import HTTPException
from http import HTTPStatus
from app.core.logger import log, LogLevel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(user_data: UserCreate, db: Session):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value, detail="E-mail já registrado"
        )
    hashed = pwd_context.hash(user_data.password)
    db_user = User(email=user_data.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    try:
        log_event.delay(str(db_user.id), LogAction.REGISTER, {"email": db_user.email})
        log(LOG_SEND_MSG, level=LogLevel.INFO)
    except Exception:
        log("Erro ao enviar log async: {e}", level=LogLevel.ERROR)
    return db_user


def login_user(user_data: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user or not pwd_context.verify(user_data.password, db_user.password):
        log(f"Falha de login para o usuário: {user_data.email}", level=LogLevel.WARNING)
        raise ValueError("Credenciais inválidas")
    token = create_access_token(
        {"sub": str(db_user.id), "email": db_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_login_total.inc()
    try:
        log_event.delay(str(db_user.id), LogAction.LOGIN, {"email": db_user.email})
        log(LOG_SEND_MSG, level=LogLevel.INFO)
    except Exception as e:
        log(f"Erro ao enviar log async: {e}", level=LogLevel.ERROR)
    return token
