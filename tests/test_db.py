# tests/test_db.py
import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import get_db


def test_get_db_yield_and_close():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    assert isinstance(db, Session)
    db.close()
