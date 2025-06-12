# TaskFlow

Projeto de aprendizado construído com FastAPI, PostgreSQL, MongoDB, Celery, RabbitMQ, Prometheus, Grafana e Docker.

## Objetivo

Aprender a construir um projeto web moderno do zero, com autenticação, APIs REST, banco relacional e NoSQL, processamento assíncrono, métricas e monitoramento.

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [MongoDB](https://www.mongodb.com/)
- [Celery](https://docs.celeryq.dev/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Docker & Docker Compose](https://www.docker.com/)
- [SQLAlchemy + Alembic](https://www.sqlalchemy.org/)
- [Pytest (futuro)](https://docs.pytest.org/)

## Como rodar localmente

### Pré-requisitos
- Docker + Docker Compose
- Git
- Python 3.11 (para desenvolvimento local)

### Passos

```bash
git clone https://github.com/douglasppa/taskflow.git
cd taskflow
cp .env.example .env  # (caso você crie esse arquivo)
docker compose up --build