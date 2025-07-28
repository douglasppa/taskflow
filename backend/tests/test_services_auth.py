import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.services import auth
from app.main import app
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from http import HTTPStatus
from passlib.context import CryptContext
from unittest.mock import patch
from app.core.logger import LogLevel
from app.auth.auth_handler import create_access_token


client = TestClient(app)

def make_fake_user(email="test@example.com", password="123456"):
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd.hash(password)
    return User(id=1, email=email, password=hashed)


# ------------------------
# Tests for register_user
# ------------------------


def test_register_user_success(db_session: Session):
    user_data = UserCreate(email="newuser@example.com", password="secret")

    with patch("app.services.auth.log_event.delay"):
        new_user = auth.register_user(user_data, db_session)

    assert new_user.email == user_data.email
    assert new_user.id is not None


def test_register_user_existing_email(db_session: Session):
    existing = User(email="duplicate@example.com", password="hashed")
    db_session.add(existing)
    db_session.commit()

    user_data = UserCreate(email="duplicate@example.com", password="newpass")

    with pytest.raises(Exception) as e:
        auth.register_user(user_data, db_session)

    assert e.value.status_code == HTTPStatus.CONFLICT
    assert "já registrado" in str(e.value.detail)


def test_register_user_log_fails(db_session: Session, capsys):
    user_data = UserCreate(email="logfail@example.com", password="fail")

    with patch("app.services.auth.log_event.delay", side_effect=Exception("Log error")):
        new_user = auth.register_user(user_data, db_session)

    assert new_user.email == user_data.email
    captured = capsys.readouterr()
    assert "Erro ao enviar log async" in captured.out


# ------------------------
# Tests for login_user
# ------------------------


def test_login_user_success(db_session: Session):
    plain_password = "abc123"
    user = make_fake_user(password=plain_password)
    db_session.add(user)
    db_session.commit()

    login = UserLogin(email=user.email, password=plain_password)

    with patch("app.services.auth.log_event.delay"):
        token = auth.login_user(login, db_session)

    assert isinstance(token, str)
    assert len(token) > 10


def test_login_user_wrong_password(db_session: Session):
    user = make_fake_user(password="abc123")
    db_session.add(user)
    db_session.commit()

    login = UserLogin(email=user.email, password="wrongpass")

    with pytest.raises(ValueError) as e:
        auth.login_user(login, db_session)

    assert "Credenciais inválidas" in str(e.value)


def test_login_user_not_found(db_session: Session):
    login = UserLogin(email="nonexistent@example.com", password="whatever")

    with pytest.raises(ValueError) as e:
        auth.login_user(login, db_session)

    assert "Credenciais inválidas" in str(e.value)


def test_login_user_log_fails(db_session: Session, capsys):
    plain_password = "abc123"
    user = make_fake_user(email="loglogin@example.com", password=plain_password)
    db_session.add(user)
    db_session.commit()

    login = UserLogin(email=user.email, password=plain_password)

    with patch("app.services.auth.log_event.delay", side_effect=Exception("Log error")):
        token = auth.login_user(login, db_session)

    assert isinstance(token, str)
    captured = capsys.readouterr()
    assert "Erro ao enviar log async" in captured.out


def test_login_user_google_existing_user(db_session: Session):
    user = User(email="google@example.com", password="")
    db_session.add(user)
    db_session.commit()

    token = "mock_token"
    mock_google_response = {"email": user.email}

    with patch("requests.get") as mock_get, patch(
        "app.services.auth.create_access_token"
    ) as mock_jwt, patch("app.services.auth.log_event.delay"):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_google_response
        mock_jwt.return_value = "jwt-token"

        jwt = auth.login_user_google(token, db_session)
        assert jwt == "jwt-token"


def test_login_user_google_new_user(db_session: Session):
    email = "newuser@google.com"
    token = "mock_token"
    mock_response = {"email": email}

    with patch("requests.get") as mock_get, patch(
        "app.services.auth.create_access_token"
    ) as mock_jwt, patch("app.services.auth.log_event.delay"), patch(
        "app.services.auth.log"
    ):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        mock_jwt.return_value = "jwt-token"

        jwt = auth.login_user_google(token, db_session)
        assert jwt == "jwt-token"


def test_login_user_google_invalid_token(db_session: Session):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 401
        with pytest.raises(HTTPException) as e:
            auth.login_user_google("invalid_token", db_session)
        assert e.value.status_code == HTTPStatus.UNAUTHORIZED
        assert "Token inválido" in e.value.detail


def test_login_user_google_missing_email(db_session: Session):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        with pytest.raises(HTTPException) as e:
            auth.login_user_google("token", db_session)
        assert e.value.status_code == HTTPStatus.BAD_REQUEST
        assert "E-mail não encontrado" in e.value.detail


def test_login_user_google_log_event_register_fails(db_session: Session):
    email = "logfail@google.com"
    token = "mock_token"
    mock_response = {"email": email}

    with patch("requests.get") as mock_get, patch(
        "app.services.auth.create_access_token"
    ) as mock_jwt, patch(
        "app.services.auth.log_event.delay", side_effect=Exception("Erro log")
    ), patch(
        "app.services.auth.log"
    ) as mock_log:

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        mock_jwt.return_value = "jwt-token"

        jwt = auth.login_user_google(token, db_session)

        mock_log.assert_any_call(
            "Erro ao logar registro social: Erro log", level=LogLevel.ERROR
        )

        assert jwt == "jwt-token"


def test_generate_reset_token_success():
    email = "user@example.com"
    with patch(
        "app.services.auth.create_access_token", return_value="token123"
    ) as mock_token, patch("app.services.auth.send_reset_email") as mock_send_email:

        result = auth.generate_reset_token(email)

        assert result == "token123"
        mock_token.assert_called_once()
        mock_send_email.assert_called_once_with(email, "token123")


def test_generate_reset_token_error():
    with patch(
        "app.services.auth.create_access_token", side_effect=Exception("fail")
    ), patch("app.services.auth.log"):
        with pytest.raises(HTTPException) as e:
            auth.generate_reset_token("x@x.com")

        assert e.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Erro ao gerar token" in str(e.value.detail)


def test_verify_reset_token_valid():
    token = create_access_token({"email": "x@x.com", "reset": True})
    email = auth.verify_reset_token(token)
    assert email == "x@x.com"


def test_verify_reset_token_invalid_payload():
    token = create_access_token({"email": "x@x.com"})  # missing 'reset'
    with pytest.raises(HTTPException) as e:
        auth.verify_reset_token(token)
    assert e.value.status_code == HTTPStatus.BAD_REQUEST


def test_verify_reset_token_internal_error(monkeypatch):
    monkeypatch.setattr("app.services.auth.verify_access_token", lambda _: 1 / 0)
    with pytest.raises(HTTPException) as e:
        auth.verify_reset_token("abc.def.ghi")
    assert e.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_reset_user_password_success(db_session: Session):
    email = "resetme@example.com"
    user = User(email=email, password="abc")
    db_session.add(user)
    db_session.commit()

    token = create_access_token({"email": email, "reset": True})

    with patch("app.services.auth.log_event.delay"), patch(
        "app.services.auth.send_updated_email"
    ):
        auth.reset_user_password(token, "novaSenha123", db_session)

    updated_user = db_session.query(User).filter_by(email=email).first()
    assert updated_user.password != "abc"


def test_reset_user_password_user_not_found(db_session: Session):
    token = create_access_token({"email": "ghost@none.com", "reset": True})
    with pytest.raises(HTTPException) as e:
        auth.reset_user_password(token, "novaSenha", db_session)
    assert e.value.status_code == HTTPStatus.NOT_FOUND


def test_reset_user_password_email_fail(db_session: Session):
    email = "confirmfail@example.com"
    user = User(email=email, password="xyz")
    db_session.add(user)
    db_session.commit()

    token = create_access_token({"email": email, "reset": True})

    with patch(
        "app.services.auth.send_updated_email", side_effect=Exception("mail fail")
    ), patch("app.services.auth.log_event.delay"), patch(
        "app.services.auth.log"
    ) as mock_log:

        auth.reset_user_password(token, "novaSenha", db_session)

        mock_log.assert_any_call(
            "Erro ao enviar e-mail de confirmação de senha: mail fail",
            level=auth.LogLevel.ERROR,
        )


@patch("app.services.auth.verify_reset_token", side_effect=ValueError("Falha inesperada"))
def test_reset_password_generic_exception(mock_verify):
    payload = {
        "token": "qualquer_token",
        "new_password": "novaSenhaSegura123"
    }
    response = client.post("/api/v1/auth/reset-password", json=payload)
    
    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno ao redefinir senha"
