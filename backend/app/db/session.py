from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import quote_plus

# Escapa variáveis sensíveis (ex: senha com @ ou :)
user = quote_plus(settings.POSTGRES_USER)
password = quote_plus(settings.POSTGRES_PASSWORD)
db_name = quote_plus(settings.POSTGRES_DB)

# Resolve o host de forma segura: "localhost" para testes, "postgres" para outros
postgres_host = settings.POSTGRES_HOST or (
    "localhost" if settings.ENVIRONMENT == "test" else "postgres"
)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{user}:{password}@{postgres_host}:{settings.POSTGRES_PORT}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
