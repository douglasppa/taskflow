from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .auth_handler import verify_access_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        payload = verify_access_token(token)
        if payload is None:
            raise HTTPException(status_code=403, detail="Token inválido ou expirado")
        return payload