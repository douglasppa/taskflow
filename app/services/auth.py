from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.constants.actions import LogAction
from app.auth.auth_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.workers.logging_tasks import log_event

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user_data: UserCreate, db: Session):
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("E-mail já registrado")
    hashed = pwd_context.hash(user_data.hashed_password)
    db_user = User(email=user_data.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    log_event.delay(str(db_user.id), LogAction.REGISTER, {"email": db_user.email})
    return db_user

def login_user(user_data: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user or not pwd_context.verify(user_data.hashed_password, db_user.hashed_password):
        raise ValueError("Credenciais inválidas")
    token = create_access_token(
        {"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    log_event.delay(str(db_user.id), LogAction.LOGIN, {"email": db_user.email})
    return token