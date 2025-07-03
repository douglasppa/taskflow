from http import HTTPStatus
from unittest.mock import patch, MagicMock
from app.db.session import get_db
from app.core.config import settings, FeatureFlags


# ==============================================================================
# GET /health/live
# ==============================================================================


def test_liveness_success(client):
    response = client.get("/api/v1/health/live")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "alive"}


# ==============================================================================
# GET /health/ready
# ==============================================================================


def test_readiness_all_services_ok(client):
    mock_client = MagicMock()
    mock_client.server_info.return_value = {}

    with patch(
        "app.api.v1.routes_monitoring.get_sync_mongo_db",
        return_value=(MagicMock(), mock_client),
    ), patch("app.api.v1.routes_monitoring.pika.BlockingConnection") as mock_rabbit:

        mock_rabbit.return_value = MagicMock()

        response = client.get("/api/v1/health/ready")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["status"] == "ready"


def test_readiness_postgresql_error(client, app_with_overrides):
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("PostgreSQL error")

    def override_get_db():
        yield mock_db

    app_with_overrides.dependency_overrides[get_db] = override_get_db

    response = client.get("/api/v1/health/ready")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "degraded"
    assert any("PostgreSQL" in e for e in response.json()["errors"])

    app_with_overrides.dependency_overrides.clear()


def test_readiness_mongodb_error(client):
    mock_client = MagicMock()
    mock_client.server_info.side_effect = Exception("MongoDB error")

    with patch(
        "app.api.v1.routes_monitoring.get_sync_mongo_db",
        return_value=(MagicMock(), mock_client),
    ):
        response = client.get("/api/v1/health/ready")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["status"] == "degraded"
        assert any("MongoDB" in e for e in response.json()["errors"])


def test_readiness_rabbitmq_error(client):
    with patch("app.api.v1.routes_monitoring.pika.BlockingConnection") as mock_rabbit:
        mock_rabbit.side_effect = Exception("RabbitMQ error")

        response = client.get("/api/v1/health/ready")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["status"] == "degraded"
        assert any("RabbitMQ" in e for e in response.json()["errors"])


# ==============================================================================
# GET /info
# ==============================================================================


def test_app_info_success(client):
    response = client.get("/api/v1/info")
    assert response.status_code == HTTPStatus.OK
    json = response.json()
    assert "app_name" in json
    assert "version" in json
    assert "environment" in json
    assert "feature_flags" in json


def test_app_info_feature_flag_error(client):
    with patch("app.api.v1.routes_monitoring.settings", settings):
        with patch.object(
            FeatureFlags,
            "model_dump",
            side_effect=Exception("Erro ao acessar features"),
        ):
            response = client.get("/api/v1/info")
            assert response.status_code == HTTPStatus.OK
            assert (
                response.json()["feature_flags"]["error"] == "Erro ao acessar features"
            )
