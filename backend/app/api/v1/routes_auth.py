from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth import (
    register_user,
    login_user,
    login_user_google,
    generate_reset_token,
    reset_user_password,
)
from http import HTTPStatus
from app.core.logger import log, LogLevel


router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleToken(BaseModel):
    token: str


@router.post("/register", summary="Register a new user", status_code=HTTPStatus.CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        register_user(user, db)
        return {"msg": "Usuário criado com sucesso"}
    except HTTPException as e:
        log("Erro ao registrar usuário", level=LogLevel.ERROR)
        raise e
    except Exception:
        log("Erro interno no servidor ao registrar usuário", LogLevel.ERROR)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor",
        )


@router.post("/login", summary="Login a user", status_code=HTTPStatus.OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login_user(user, db)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        log(f"Falha de login para o usuário {user.email}: {str(e)}", LogLevel.ERROR)
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail=str(e))


@router.post(
    "/google", summary="Google OAuth authentication", status_code=HTTPStatus.OK
)
async def login_google(data: GoogleToken, db: Session = Depends(get_db)):
    try:
        token = login_user_google(data.token, db)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        log("Erro HTTP durante login com Google", level=LogLevel.ERROR)
        raise e
    except Exception as e:
        log(f"Erro interno no login Google: {e}", level=LogLevel.ERROR)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar autenticação Google",
        )


@router.post("/forgot-password", summary="Request password reset")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        generate_reset_token(data.email)
        return {"message": "E-mail enviado com instruções para redefinir a senha"}
    except HTTPException as e:
        log(
            f"Erro ao solicitar redefinição (HTTPException): {e.detail}",
            level=LogLevel.WARNING,
        )
        raise e
    except Exception as e:
        log(f"Erro interno ao solicitar redefinição: {e}", level=LogLevel.ERROR)
        raise HTTPException(status_code=500, detail="Erro interno ao gerar token")


@router.post("/reset-password", summary="Reset user password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_user_password(data.token, data.new_password, db)
        return {"message": "Senha redefinida com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        log(f"Erro interno ao redefinir senha: {e}", level=LogLevel.ERROR)
        raise HTTPException(status_code=500, detail="Erro interno ao redefinir senha")
