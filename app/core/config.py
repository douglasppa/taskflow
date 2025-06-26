from pydantic_settings import BaseSettings
import os
from pathlib import Path
import logging
from pydantic import Field


def get_app_version() -> str:
    logger = logging.getLogger(__name__)
    try:
        base_dir = Path(__file__).resolve().parent.parent  # /app/app
        version_path = base_dir.parent / "VERSION"  # /app/VERSION
        logger.info(f"App Version: {version_path.read_text().strip()}")
        return version_path.read_text().strip()
    except Exception as e:
        logger.warning(f"Failed to read VERSION file: {e}")
        return "0.0.0"


class FeatureFlags(BaseSettings):
    simulate_task_latency: bool = Field(default=False)
    enable_summary_endpoint: bool = Field(default=False)

    class Config:
        env_prefix = "FEATURE_"
        extra = "ignore"


class Settings(BaseSettings):
    # Application settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TaskFlow"
    APP_VERSION: str = Field(default_factory=get_app_version)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # PostgreSQL connection
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "taskflow")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "secret")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "taskflow_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)

    # Authentication settings
    SECRET_KEY: str
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # RabbitMQ connection
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS", "guest")

    # MongoDB connection
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://mongo_db:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "taskflow")
    MONGO_DB_ATLAS_USER: str | None = None
    MONGO_DB_ATLAS_PASSWORD: str | None = None

    # Prometheus settings
    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT", 8000))

    features: FeatureFlags = FeatureFlags()

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
