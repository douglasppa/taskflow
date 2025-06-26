from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth import register_user, login_user
from http import HTTPStatus
from app.core.logger import log

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", summary="Register a new user", status_code=HTTPStatus.CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        register_user(user, db)
        return {"msg": "Usuário criado com sucesso"}
    except HTTPException as e:
        log("Erro ao registrar usuário", level="ERROR")
        raise e
    except Exception:
        log("Erro interno no servidor ao registrar usuário", level="ERROR")
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
        log(f"Falha de login para o usuário {user.username}: {str(e)}", level="ERROR")
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail=str(e))
