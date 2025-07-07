# tests/test_db.py

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.mongo import get_mongo_db
from app.core.config import settings


def test_get_db_yield_and_close():
    """Testa se o get_db() retorna uma sessão SQLAlchemy válida e fecha corretamente."""
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)
    db.close()


def test_get_mongo_db_returns_async_db():
    """Testa se o get_mongo_db() retorna o banco MongoDB com o nome correto."""
    db = get_mongo_db()
    assert db.name == settings.MONGO_DB_NAME
