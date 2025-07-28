from http import HTTPStatus
from fastapi import HTTPException
from unittest.mock import patch
from app.auth.auth_handler import create_access_token
from app.models.user import User

FORGOT_URL = "/api/v1/auth/forgot-password"
RESET_URL = "/api/v1/auth/reset-password"


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


def test_google_login_success(client):
    valid_token = "valid_token"

    with patch("app.api.v1.routes_auth.login_user_google") as mocked_login:
        mocked_login.return_value = "fake-jwt-token"

        response = client.post("/api/v1/auth/google", json={"token": valid_token})
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json()


def test_google_login_http_exception(client):
    with patch("app.api.v1.routes_auth.login_user_google") as mocked_login:
        mocked_login.side_effect = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Token inválido"
        )
        response = client.post("/api/v1/auth/google", json={"token": "invalid"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["detail"] == "Token inválido"


def test_google_login_internal_error(client):
    with patch(
        "app.api.v1.routes_auth.login_user_google", side_effect=Exception("Erro")
    ):
        response = client.post("/api/v1/auth/google", json={"token": "whatever"})
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert (
            response.json()["detail"] == "Erro interno ao processar autenticação Google"
        )


def test_forgot_password_success(client, db_session):
    # Arrange: cria usuário
    email = "reset@example.com"
    user = User(email=email, password="hashed")
    db_session.add(user)
    db_session.commit()

    # Act
    response = client.post(FORGOT_URL, json={"email": email})

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert "instruções" in response.json()["message"].lower()


def test_forgot_password_invalid_email_format(client):
    response = client.post(FORGOT_URL, json={"email": "invalido"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@patch(
    "app.api.v1.routes_auth.generate_reset_token",
    side_effect=Exception("Erro genérico"),
)
def test_forgot_password_unexpected_error(mock_generate, client):
    response = client.post(
        "/api/v1/auth/forgot-password", json={"email": "teste@teste.com"}
    )
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Erro interno ao gerar token" in response.text


def test_reset_password_success(client, db_session):
    email = "user@example.com"
    password = "antiga"
    user = User(email=email, password=password)
    db_session.add(user)
    db_session.commit()

    # Gera token de reset
    token = create_access_token({"email": email, "reset": True})

    response = client.post(
        RESET_URL, json={"token": token, "new_password": "novasenha123"}
    )

    assert response.status_code == HTTPStatus.OK
    assert "sucesso" in response.json()["message"].lower()


def test_reset_password_invalid_token(client):
    response = client.post(
        RESET_URL, json={"token": "token.invalido.aqui", "new_password": "123456"}
    )
    assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.BAD_REQUEST]
    assert "token" in response.json()["detail"].lower()


def test_reset_password_missing_field(client):
    response = client.post(
        RESET_URL, json={"token": "abc"}  # falta o campo new_password
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@patch(
    "app.api.v1.routes_auth.reset_user_password", side_effect=Exception("Erro interno")
)
def test_reset_password_internal_error(mock_reset, client):
    response = client.post(
        "/api/v1/auth/reset-password", json={"token": "dummy", "new_password": "abc123"}
    )
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Erro interno ao redefinir senha" in response.text
