# 📄 CHANGELOG

All notable changes to this project will be documented here.

## 📦 v1.2.0 – Google OAuth login  
**Date:** 2025-07-25

### 🔐 Authentication
- Added new route `/api/v1/auth/google` to support login with Google accounts via OAuth.
- Implemented `login_user_google` service to validate ID tokens with Google, create users if necessary, and issue JWTs.

### 🧪 Testing
- Created unit and integration tests for the Google login API, achieving **100% coverage** for the new functionality.
- Handled edge cases such as invalid tokens, missing email in payload, and logging failures during registration and login.

## 📦 v1.1.1 – JWT authentication flow  
**Date:** 2025-07-05

### 🔧 Backend adjustments
- Updated JWT payload to include `email` in addition to `sub` (user ID).
- Minor improvements to `create_access_token` to support custom payloads.


## 📦 v1.1.0 – Full test coverage and quality analysis  
**Date:** 2025-07-03

### 📊 Code quality and static analysis
- Integrated [SonarCloud](https://sonarcloud.io/) for code quality analysis, test coverage, and code smells.
- Configured the project to report test coverage using `pytest-cov`.
- Fixed all critical issues identified by Sonar, including code duplication, unused variables, and deprecated practices.

### 🧪 Testing
- Added new unit and integration tests to achieve **100% coverage**.
- Tests for monitoring routes (`/health/ready`) covering MongoDB and RabbitMQ failure scenarios.
- Tests for asynchronous event logging with MongoDB persistence validation.

### 🔧 Refactors and technical adjustments
- Refactored the logging service (`logger.py`) to consistently use `LogLevel` constants.
- Extracted MongoDB connection instances (`motor` and `pymongo`) into reusable functions in `app.db.mongo`.
- Replaced direct `MongoClient` access with centralized `get_sync_mongo_db()` calls to improve testability.
- Adjusted `pytest.ini` to avoid warnings related to `env_files`, and migrated from `Config` to `ConfigDict` (Pydantic v2).

### 🧼 Cleanup and maintenance
- Removed redundant code and added safeguards against silent failures in generic exceptions.
- Updated dependencies with a warning about the deprecation of `crypt` in Python 3.13.
- Organized imports and standardized internal technical logs and error messages.


## 📦 v1.0.0 – Cloud deploy and CI/CD  
**Date:** 2025-06-26

### 🚀 Features
- App versioning via `VERSION` file reading.
- Created `/info` endpoint returning app version and mode.
- Created `/summary` endpoint returning total tasks per user (controlled by feature flag).
- Introduced feature flags via config file to control feature availability.

### 🔧 Technical adjustments
- Fixed logging setup with centralized configuration and consistent formatting.
- Added dummy Celery worker to comply with Render’s free plan.

### ☁️ Deploy and Continuous Integration
- Configured deployment on [Render](https://render.com/) with MongoDB Atlas and CloudAMQP support.
- Created GitHub Actions pipeline:
  - Running `flake8` for lint checks.
  - Executing tests with `pytest` before automatic deployment.


## 📦 v0.3.0 – Observability and monitoring  
**Date:** 2025-06-20

### ✨ New features
- Integrated Prometheus for exporting API metrics.
- Configured base dashboard in Grafana for visualizing operational data.
- Monitoring endpoints:
  - `/metrics`: exposes Prometheus metrics.
  - `/health/live`: liveness probe.
  - `/health/ready`: readiness check for external dependencies (PostgreSQL, MongoDB, RabbitMQ).
- Structured logging in JSON format to facilitate log analysis and tracing.
- Custom Prometheus counters:
  - `task_created_total`
  - `user_login_total`

### 🧪 Testing
- Added automated tests for:
  - Authentication
  - Tasks
  - Healthchecks
- Isolated test setup using `pytest` and `httpx`.
- Adjusted test execution in Docker environment.

### 🛠️ Structure and documentation
- Added explanatory comments in `schemas/` files.
- Included `pydeps` tool to visualize module dependencies.
- Created `docs/contracts.md` documenting REST contracts and async payloads via Celery.
- Refined routes and tag grouping in Swagger documentation.


## 📦 v0.2.0 – Authentication and async tasks  
**Date:** 2025-06-13

### 🚀 Features
- Implemented JWT-based authentication: user registration and login with token generation.
- Restricted access to tasks: users can only view, edit, and delete their own tasks.
- User action and task logging using MongoDB.
- Integrated Celery and RabbitMQ for asynchronous event logging.

### 🛠 Infrastructure
- Configured Celery worker in `docker-compose.yml`.
- Explicit task registration in `celery_app.py`.
- MongoDB connection in the worker handled via `pymongo`.
- Removed `task_routes` to ensure compatibility with Celery's default queue.

### 🔧 Other
- Added temporary print statements to aid debugging during task execution.


## 📦 v0.1.0 – CRUD working  
**Date:** 2025-06-12

### 🚀 Features
- Implemented full task CRUD with FastAPI.
- REST endpoints integrated with PostgreSQL.
- Swagger UI enabled.

### 🛠 Infrastructure
- Initial setup with Docker and Alembic.
- Modular structure: `models`, `schemas`, `routes`, `services`.

### 🔧 Other
- Initial database and migration setup.
