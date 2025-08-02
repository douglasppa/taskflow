from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.constants.actions import LogAction
from app.services.email import send_reset_email, send_updated_email
from app.auth.auth_handler import create_access_token, verify_access_token
from app.workers.logging_tasks import log_event
from app.core.metrics import user_login_total
from app.core.config import settings
from app.constants.actions import LOG_SEND_MSG
from fastapi import HTTPException
from http import HTTPStatus
from app.core.logger import log, LogLevel

import requests

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


def login_user_google(token: str, db: Session):
    # Verifica token com o Google
    response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
    )
    if response.status_code != 200:
        log("Token Google inválido", level=LogLevel.WARNING)
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value, detail="Token inválido"
        )

    payload = response.json()
    email = payload.get("email")
    if not email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value, detail="E-mail não encontrado"
        )

    # Busca ou cria usuário
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, password="")  # senha vazia
        db.add(user)
        db.commit()
        db.refresh(user)
        try:
            log_event.delay(str(user.id), LogAction.REGISTER, {"email": user.email})
            log(LOG_SEND_MSG, level=LogLevel.INFO)
        except Exception as e:
            log(f"Erro ao logar registro social: {e}", level=LogLevel.ERROR)

    # Gera token JWT
    token = create_access_token(
        {"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_login_total.inc()

    try:
        log_event.delay(str(user.id), LogAction.LOGIN, {"email": user.email})
        log(LOG_SEND_MSG, level=LogLevel.INFO)
    except Exception as e:
        log(f"Erro ao logar login social: {e}", level=LogLevel.ERROR)

    return token


def generate_reset_token(email: str) -> str:
    try:
        token = create_access_token(
            {"email": email, "reset": True},
            expires_delta=timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES),
        )
        send_reset_email(email, token)
        log(f"Token de redefinição gerado para {email}", level=LogLevel.INFO)
        return token
    except Exception as e:
        log(
            f"Erro ao gerar token de redefinição para {email}: {e}",
            level=LogLevel.ERROR,
        )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar token de redefinição",
        )


def verify_reset_token(token: str) -> str:
    try:
        payload = verify_access_token(token)
        if not payload.get("reset") or not payload.get("email"):
            log("Token de redefinição inválido", level=LogLevel.WARNING)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Token de redefinição inválido",
            )
        return payload["email"]
    except HTTPException as e:
        raise e
    except Exception as e:
        log(f"Erro ao verificar token de redefinição: {e}", level=LogLevel.ERROR)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar token",
        )


def reset_user_password(token: str, new_password: str, db: Session):
    try:
        email = verify_reset_token(token)

        user = db.query(User).filter(User.email == email).first()
        if not user:
            log(
                f"Tentativa de redefinição para usuário inexistente: {email}",
                level=LogLevel.WARNING,
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
            )

        hashed = pwd_context.hash(new_password)
        user.password = hashed
        db.commit()

        try:
            log_event.delay(
                str(user.id), LogAction.RESET_PASSWORD, {"email": user.email}
            )
        except Exception as log_err:
            log(
                f"Erro ao registrar log de redefinição: {log_err}", level=LogLevel.ERROR
            )
        log(LOG_SEND_MSG, level=LogLevel.INFO)

        try:
            send_updated_email(user.email)
        except Exception as e:
            log(
                f"Erro ao enviar e-mail de confirmação de senha: {e}",
                level=LogLevel.ERROR,
            )

        log(f"Senha redefinida com sucesso para {email}", level=LogLevel.INFO)

    except HTTPException as e:
        raise e
    except Exception as e:
        log(f"Erro interno ao redefinir senha: {e}", level=LogLevel.WARNING)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno ao redefinir senha",
        )
