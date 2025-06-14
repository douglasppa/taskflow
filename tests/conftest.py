import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import get_db  # ajuste conforme a localização
from app.workers.celery_app import celery_app

# Ativa execução síncrona do Celery nos testes
celery_app.conf.task_always_eager = True

# Banco em memória (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria o schema na memória
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Inicia uma transação antes do teste e faz rollback ao final."""
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
def client(db_session):
    """Cria um client FastAPI com DB isolado para cada teste."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c