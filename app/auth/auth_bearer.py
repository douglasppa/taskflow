from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .auth_handler import verify_access_token
from http import HTTPStatus


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Credenciais de autenticação ausentes",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        payload = verify_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        request.state.user = payload  # útil para middlewares, logs etc.
        return payload
