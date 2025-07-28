# tests/conftest.py
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from dotenv import load_dotenv

from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.models.user import User
from app.services.auth import pwd_context
from app.workers.celery_app import celery_app

# Carrega variáveis de ambiente específicas para testes
load_dotenv(".env.test")

# Configura o Celery para execução síncrona nos testes
celery_app.conf.task_always_eager = True

# Banco SQLite em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas no início
Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def disable_celery_log_event():
    """Desativa o envio real de tarefas Celery de logging."""
    with patch("app.workers.logging_tasks.log_event.delay") as mock_task:
        yield mock_task


@pytest.fixture(scope="function")
def db_session():
    """Garante transações isoladas por teste (rollback ao final)."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def app_with_overrides(db_session):
    """Exponibiliza o app com as dependências do banco sobrescritas."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(app_with_overrides):
    """Cria um TestClient com banco isolado e overrides aplicados."""
    with TestClient(app_with_overrides) as c:
        yield c


@pytest.fixture
def create_user(db_session: Session):
    user = User(email="reset@example.com", password=pwd_context.hash("senha123"))
    db_session.add(user)
    db_session.commit()
    return user
