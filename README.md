# TaskFlow

[![Build](https://github.com/douglasppa/taskflow/actions/workflows/ci.yml/badge.svg)](https://github.com/douglasppa/taskflow/actions/workflows/ci.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=douglasppa_taskflow&metric=coverage)](https://sonarcloud.io/dashboard?id=douglasppa_taskflow)
![GitHub tag](https://img.shields.io/github/v/tag/douglasppa/taskflow)

**TaskFlow** is a learning-oriented fullstack project built with **FastAPI**, **React**, **PostgreSQL**, **MongoDB**, **Celery**, **RabbitMQ**, **Prometheus**, **Grafana**, **Docker**, **GitHub Actions**, **Render**, and **Vercel**.

This monorepo demonstrates how to build, test, observe, and deploy a modern web application using technologies commonly required in engineering leadership and software development roles.

---

## 🌟 Objectives

Learn how to build and operate a complete modern web project, covering:

- 🔐 JWT Authentication and OAuth login with Google
- 📦 RESTful APIs with full CRUD support
- 🧠 Relational database with PostgreSQL
- 📄 NoSQL storage for logging via MongoDB
- 🕒 Asynchronous event processing with Celery + RabbitMQ
- 📈 Metrics exporting using Prometheus and Web Vitals (LCP, TTFB, INP, CLS, FCP)
- 📊 Observability dashboards with Grafana
- 🧪 Full test coverage with Pytest and Vitest
- 🧹 Linting with Ruff, Black, ESLint and Prettier
- ⚙️ CI/CD with GitHub Actions (pipeline for lint, test, coverage, SonarCloud)
- 🐳 Local development using Docker and Docker Compose
- 🚀 Deployment: Backend on Render, Frontend on Vercel
- 🎨 Responsive frontend built with React + TypeScript + Tailwind CSS

---

## 🧰 Technologies

### Backend

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [MongoDB](https://www.mongodb.com/)
- [Celery](https://docs.celeryq.dev/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [SQLAlchemy + Alembic](https://www.sqlalchemy.org/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Pytest](https://docs.pytest.org/)
- [Ruff](https://docs.astral.sh/ruff/) + [Black](https://black.readthedocs.io/)
- [Docker & Docker Compose](https://www.docker.com/)
- [Render](https://render.com/)

### Frontend

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Router](https://reactrouter.com/)
- [Axios](https://axios-http.com/)
- [ESLint](https://eslint.org/) + [Prettier](https://prettier.io/)
- [Vitest](https://vitest.dev/)
- [Lucide Icons](https://lucide.dev/)
- [Vercel](https://vercel.com/)

---

## 🚀 Running the project locally

### Prerequisites

- [Docker](https://www.docker.com/) + Docker Compose
- [Git](https://git-scm.com/)
- Python 3.11+ (optional, for local backend dev)
- Node.js 18+ (optional, for local frontend dev)

### Quick start

```bash
git clone https://github.com/douglasppa/taskflow.git
cd taskflow
cp .env.example .env
docker-compose -f docker-compose.dev.yml up -d --build
```

🧪 API available at: http://localhost:8000/docs
🎨 Frontend runs at: http://localhost:5173

## 📬 API Endpoints
| Method   | Path                    | Description                           |
| -------- | ----------------------- | ------------------------------------- |
| GET      | `/metrics`              | Prometheus metrics                    |
| GET      | `/health/live`          | Liveness probe                        |
| GET      | `/health/ready`         | Readiness check                       |
| GET      | `/info`                 | App version and mode                  |
| POST     | `/auth/register`        | Register new user                     |
| POST     | `/auth/login`           | Login with email and password         |
| POST     | `/auth/google`          | OAuth login with Google               |
| POST     | `/auth/forgot-password` | Request password reset token          |
| POST     | `/auth/reset-password`  | Reset password with token             |
| GET/POST | `/tasks`                | Task list, creation, update, deletion |

## 🧪 Tests and Coverage
Backend
```bash
# Run tests with coverage
docker-compose -f docker-compose.dev.yml run --rm web coverage run --source=app -m pytest

# Generate HTML coverage report
docker-compose -f docker-compose.dev.yml run --rm web coverage html
```
Frontend
```bash
# Run unit tests
npx vitest run

# Run tests with coverage
npx vitest run --coverage
```

## 🧹 Linting and Code Style
Backend
```bash
ruff check . --fix
black .
```
Frontend
```bash
npm run lint
npx prettier --check .
```

## 🔁 CI/CD with GitHub Actions
GitHub Actions is used to:
* ✅ Lint backend (Ruff, Black) and frontend (ESLint, Prettier)
* 🧪 Run backend tests with Pytest + coverage
* 🧪 Run frontend tests with Vitest + coverage
* 📊 Analyze quality and coverage with SonarCloud
Workflows are located in .github/workflows/.

## 🚢 Deployment
- Backend: deployed via Docker on Render
  - Startup command: python -m app.main
  - Environment variables managed via .env.example
- Frontend: deployed on Vercel

## 🧭 Project Structure (Monorepo)
```bash
taskflow/
├── backend/       # FastAPI + Celery + Databases
├── frontend/      # React + Vite + Tailwind + TypeScript
├── grafana/       # Dashboards and provisioning
├── prometheus/    # Monitoring configuration
├── docker-compose.dev.yml
├── .env, .env.example
└── README.md, LICENSE, CHANGELOG.md, VERSION
```

## 🖼️ Screenshots
Here are some screens from the main screens and dashboards for TaskFlow.

### 🖥️ Web Application
Built with React, Vite, TypeScript and Tailwind CSS to provide a clean, responsive and authenticated user experience across pages like login, dashboard and task management.

<p align="center">
  <a href="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-login.png">
    <img src="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-login.png" alt="Login Screen" width="15%" />
  </a>
  <a href="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-home.png">
    <img src="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-home.png" alt="Dashboard Screen" width="40%" />
  </a>
  <a href="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-tasks.png">
    <img src="https://raw.githubusercontent.com/douglasppa/taskflow/main/frontend/src/assets/screenshot-tasks.png" alt="Task List Screen" width="40%" />
  </a>
</p>

### 📊 Monitoring Dashboards
Built with Prometheus + Grafana using metrics from backend and frontend (Web Vitals).

<p align="center">
  <a href="https://raw.githubusercontent.com/douglasppa/taskflow/main/backend/assets/grafana-api-dashboard.png">
    <img src="https://raw.githubusercontent.com/douglasppa/taskflow/main/backend/assets/grafana-api-dashboard.png" alt="Grafana API Dashboard" width="45%" />
  </a>
  <a href="https://raw.githubusercontent.com/douglasppa/taskflow/main/backend/assets/grafana-web-dashboard.png">
    <img src="https://raw.githubusercontent.com/douglasppa/taskflow/main/backend/assets/grafana-web-dashboard.png" alt="Grafana Web Dashboard" width="45%" />
  </a>
</p>

🤝 Contributions
This project is for personal learning, but contributions, ideas, and feedback are welcome! Open an issue or fork and submit a PR 🚀
