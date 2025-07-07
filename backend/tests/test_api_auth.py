from http import HTTPStatus
from fastapi import HTTPException
from unittest.mock import patch


def test_register(client):
    data = {"email": "test@example.com", "password": "test123"}

    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code in (HTTPStatus.CREATED, HTTPStatus.CONFLICT)


def test_register_raises_http_exception(client):
    data = {"email": "duplicate@example.com", "password": "test123"}

    with patch("app.api.v1.routes_auth.register_user") as mocked_register:
        mocked_register.side_effect = HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Usuário já existe"
        )

        response = client.post("/api/v1/auth/register", json=data)
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()["detail"] == "Usuário já existe"


def test_register_internal_server_error(client):
    data = {"email": "fail@example.com", "password": "test123"}

    with patch(
        "app.api.v1.routes_auth.register_user",
        side_effect=Exception("Falha inesperada"),
    ):
        response = client.post("/api/v1/auth/register", json=data)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()["detail"] == "Erro interno no servidor"


def test_login_valid_credentials(client):
    data = {"email": "test@example.com", "password": "test123"}

    client.post("/api/v1/auth/register", json=data)

    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()


def test_login_invalid_credentials(client):
    invalid_data = {"email": "wrong@example.com", "password": "wrongpass"}

    response = client.post("/api/v1/auth/login", json=invalid_data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "Credenciais inválidas"
