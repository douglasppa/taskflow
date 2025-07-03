import pytest
from sqlalchemy.orm import Session
from app.services import auth
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from http import HTTPStatus
from passlib.context import CryptContext
from unittest.mock import patch


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
