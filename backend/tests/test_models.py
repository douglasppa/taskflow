import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.task import Task
from app.db.base import Base

# Banco de dados em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação do schema
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def test_create_user(db_session):
    user = User(email="test@example.com", password="secret")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None
    assert user.email == "test@example.com"


def test_create_task(db_session):
    user = User(email="owner@example.com", password="ownerpass")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task = Task(title="Test Task", description="Descrição", owner_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.owner_id == user.id
    assert task.owner.email == "owner@example.com"


def test_user_repr():
    user = User(id=1, email="user@example.com", password="123")
    assert repr(user) == "<User id=1 email=user@example.com>"


def test_task_repr():
    task = Task(id=42, title="Sample", description="Desc", owner_id=1)
    assert repr(task) == "<Task id=42 title=Sample>"
