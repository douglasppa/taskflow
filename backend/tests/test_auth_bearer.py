import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.auth.auth_bearer import JWTBearer
from unittest.mock import AsyncMock, patch, MagicMock
from http import HTTPStatus


# ==============================================================================
# JWTBearer - Testes Unitários
# ==============================================================================


@pytest.mark.asyncio
async def test_jwtbearer_missing_credentials():
    bearer = JWTBearer()

    mock_request = MagicMock()
    # Simula retorno vazio do super().__call__()
    with patch(
        "fastapi.security.HTTPBearer.__call__", new=AsyncMock(return_value=None)
    ):
        with pytest.raises(HTTPException) as exc_info:
            await bearer(mock_request)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "ausentes" in exc_info.value.detail


@pytest.mark.asyncio
async def test_jwtbearer_invalid_token():
    bearer = JWTBearer()

    mock_request = MagicMock()
    fake_credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="invalid_token"
    )

    # Simula super().__call__ retornando credenciais, mas token inválido no verify
    with patch(
        "fastapi.security.HTTPBearer.__call__",
        new=AsyncMock(return_value=fake_credentials),
    ), patch("app.auth.auth_bearer.verify_access_token", return_value=None):

        with pytest.raises(HTTPException) as exc_info:
            await bearer(mock_request)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "inválido ou expirado" in exc_info.value.detail


@pytest.mark.asyncio
async def test_jwtbearer_valid_token():
    bearer = JWTBearer()

    mock_request = MagicMock()
    mock_request.state = MagicMock()
    fake_credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials="valid_token"
    )
    payload = {"sub": "123", "role": "user"}

    # Simula super().__call__ com token válido e verify_access_token retornando payload
    with patch(
        "fastapi.security.HTTPBearer.__call__",
        new=AsyncMock(return_value=fake_credentials),
    ), patch("app.auth.auth_bearer.verify_access_token", return_value=payload):

        result = await bearer(mock_request)

    assert result == payload
    assert mock_request.state.user == payload
