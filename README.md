# TaskFlow

Projeto de aprendizado construído com FastAPI, PostgreSQL, MongoDB, Celery, RabbitMQ, Prometheus, Grafana, Docker, GitHub Actions e Render.

## 🌟 Objetivo

Aprender a construir um projeto web moderno do zero, cobrindo:

* Autenticação com JWT
* APIs RESTful (CRUD)
* Banco de dados relacional (PostgreSQL)
* Banco NoSQL para logs (MongoDB)
* Processamento assíncrono com Celery + RabbitMQ
* Exportação de métricas com Prometheus
* Visualização com Grafana
* Contêineres com Docker
* Testes automatizados com Pytest
* Lint com Flake8
* Deploy contínuo com GitHub Actions e Render

## 🧰 Tecnologias

* [FastAPI](https://fastapi.tiangolo.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [MongoDB](https://www.mongodb.com/)
* [Celery](https://docs.celeryq.dev/)
* [RabbitMQ](https://www.rabbitmq.com/)
* [Prometheus](https://prometheus.io/)
* [Grafana](https://grafana.com/)
* [Docker & Docker Compose](https://www.docker.com/)
* [SQLAlchemy + Alembic](https://www.sqlalchemy.org/)
* [Pytest](https://docs.pytest.org/)
* [Flake8](https://flake8.pycqa.org/)
* [GitHub Actions](https://docs.github.com/en/actions)
* [Render](https://render.com/)

## 🚀 Como rodar localmente

### Pré-requisitos

* Docker + Docker Compose
* Git
* Python 3.11 (opcional, para desenvolvimento local)

### Passos

```bash
git clone https://github.com/douglasppa/taskflow.git
cd taskflow
cp .env.example .env  # ou crie o arquivo .env manualmente
docker-compose -f docker-compose.dev.yml up -d --build
```

Acesse a aplicação em [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testes e Lint

Para executar os testes automatizados com Pytest e verificar o lint com Flake8:

```bash
docker-compose -f docker-compose.dev.yml exec web pytest
flake8 .
```

## 🔁 Integração Contínua com GitHub Actions

Este projeto utiliza GitHub Actions para:

* Rodar o lint com Flake8
* Executar os testes com Pytest

O workflow está localizado em `.github/workflows/main.yml`.

## 🚢 Deploy com Render

O deploy contínuo está integrado à plataforma Render.

* O Dockerfile é utilizado para criar a imagem da aplicação
* O comando de inicialização no Render é:

  ```bash
  python -m app.main
  ```

Certifique-se de adicionar as variáveis de ambiente no painel da Render com base no arquivo `.env.example`.

---

## 📊 Monitoring Dashboard

Here’s a snapshot of the current observability dashboard in Grafana:

![Grafana Dashboard](assets/grafana-dashboard.png)

Este projeto é uma iniciativa de aprendizado e prática com tecnologias modernas de backend. Contributions e feedbacks são bem-vindos! 🚀
