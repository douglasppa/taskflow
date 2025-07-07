from datetime import datetime, timedelta, timezone
from jose import JWTError, ExpiredSignatureError, jwt
from fastapi import HTTPException
from http import HTTPStatus
from app.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value, detail="Token expirado"
        )
    except JWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value, detail="Token inválido"
        )
