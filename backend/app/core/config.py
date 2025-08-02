from pydantic_settings import BaseSettings
import os
from pathlib import Path
from pydantic import Field, ConfigDict
from app.core.logger import log, LogLevel


def get_app_version(version_path: Path = None) -> str:
    try:
        if version_path:
            app_version = version_path.read_text().strip()
        else:
            version_path = Path.cwd() / "VERSION"
            app_version = version_path.read_text().strip()
        log(f"App Version: {app_version}", level=LogLevel.INFO)
        return app_version
    except Exception as e:
        log(f"Failed to read VERSION file: {str(e)}", level=LogLevel.ERROR)
        return "0.0.0"


class FeatureFlags(BaseSettings):
    simulate_task_latency: bool = Field(default=False)
    enable_summary_endpoint: bool = Field(default=False)

    model_config = ConfigDict(env_prefix="FEATURE_", extra="ignore")


class Settings(BaseSettings):
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

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
    RESET_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 15))

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

    # Email (SMTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")

    # Frontend URL para recuperação de senha
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    features: FeatureFlags = FeatureFlags()

    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
