import pytest
from datetime import timedelta, datetime, timezone
from jose import jwt
from fastapi import HTTPException
from http import HTTPStatus

from app.auth.auth_handler import create_access_token, verify_access_token
from app.core.config import settings


# ==============================================================================
# Função: create_access_token
# ==============================================================================


def test_create_access_token_returns_valid_jwt():
    data = {"sub": "123"}
    token = create_access_token(data)

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_create_access_token_with_custom_expiration():
    data = {"sub": "abc"}
    delta = timedelta(seconds=60)
    token = create_access_token(data, expires_delta=delta)

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == "abc"
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    expected = datetime.now(timezone.utc) + delta
    assert abs((exp - expected).total_seconds()) < 5  # margem de erro


# ==============================================================================
# Função: verify_access_token
# ==============================================================================


def test_verify_access_token_valid():
    token = create_access_token({"sub": "token_ok"})
    payload = verify_access_token(token)
    assert payload["sub"] == "token_ok"


def test_verify_access_token_expired():
    data = {"sub": "expired"}
    past_delta = timedelta(seconds=-1)
    expired_token = create_access_token(data, expires_delta=past_delta)

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(expired_token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "expirado" in exc_info.value.detail


def test_verify_access_token_invalid():
    invalid_token = "abc.def.ghi"  # estrutura de JWT, mas inválido

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(invalid_token)

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert "inválido" in exc_info.value.detail
