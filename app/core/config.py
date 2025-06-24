from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TaskFlow"

    # PostgreSQL connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Authentication settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # RabbitMQ connection
    RABBITMQ_URL: str

    # MongoDB connection
    MONGO_URL: str
    MONGO_DB_NAME: str
    MONGO_DB_ATLAS_USER: str | None = None
    MONGO_DB_ATLAS_PASSWORD: str | None = None

    # Prometheus settings
    PROMETHEUS_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()