from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError, jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from http import HTTPStatus
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="Token inválido")