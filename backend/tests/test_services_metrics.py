import pytest
from unittest.mock import MagicMock, patch
from app.core.logger import LogLevel
from app.services.metrics import save_metric, update_frontend_metrics
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_save_metric_invalid_timestamp():
    fake_data = {
        "name": "FCP",
        "value": 1500,
        "delta": 40,
        "id": "789",
        "rating": "good",
        "navigationType": "navigate",
        "timestamp": "INVALID_TIMESTAMP",
    }

    mock_db = MagicMock()
    mock_client = MagicMock()

    with patch(
        "app.services.metrics.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        save_metric(fake_data)

    assert "received_at" in fake_data
    mock_db.metrics.insert_one.assert_called_once_with(fake_data)
    mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_save_metric_insert_fails_with_log():
    fake_data = {
        "name": "TTFB",
        "value": 500,
        "delta": 20,
        "id": "456",
        "rating": "needs-improvement",
        "navigationType": "back-forward",
        "timestamp": "2025-07-31T14:00:00.000Z",
    }

    mock_db = MagicMock()
    mock_client = MagicMock()
    mock_db.metrics.insert_one.side_effect = Exception("falha simulada")

    with patch(
        "app.services.metrics.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ), patch("app.services.metrics.log") as mock_log:

        with pytest.raises(HTTPException) as exc:
            save_metric(fake_data)

        assert exc.value.status_code == 400
        assert "Erro ao salvar métrica" in str(exc.value.detail)

        # Verifica se o log de erro foi chamado corretamente
        mock_log.assert_any_call(
            "Erro ao inserir métrica no MongoDB: falha simulada", level=LogLevel.ERROR
        )

        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_save_metric_client_close_fails():
    fake_data = {
        "name": "INP",
        "value": 300,
        "delta": 25,
        "id": "abc",
        "rating": "poor",
        "navigationType": "navigate",
        "timestamp": "2025-07-31T14:20:00.000Z",
    }

    mock_db = MagicMock()
    mock_client = MagicMock()
    mock_client.close.side_effect = Exception("erro ao fechar client")

    with patch(
        "app.services.metrics.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        save_metric(fake_data)

    mock_db.metrics.insert_one.assert_called_once()
    mock_client.close.assert_called_once()


@pytest.fixture
def sample_metrics():
    return [
        {"name": "LCP", "value": 1000, "route": "/home", "browser": "Chrome"},
        {"name": "LCP", "value": 2000, "route": "/home", "browser": "Chrome"},
        {"name": "CLS", "value": 0.2, "route": "/home", "browser": "Firefox"},
        {"name": "TTFB", "value": 500, "route": "/login", "browser": "Edge"},
        {"name": "FCP", "value": 800, "route": "/home", "browser": "Chrome"},
    ]


def test_update_frontend_metrics_success(sample_metrics):
    mock_db = MagicMock()
    mock_client = MagicMock()
    mock_db.metrics.find.return_value = sample_metrics

    # Mock das funções .labels().set() de cada Gauge
    mock_gauge = MagicMock()
    gauge_dict = {
        "LCP": mock_gauge,
        "CLS": mock_gauge,
        "TTFB": mock_gauge,
        "FCP": mock_gauge,
        "INP": mock_gauge,
    }

    with patch(
        "app.services.metrics.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ), patch("app.services.metrics.METRIC_NAME_TO_GAUGE", gauge_dict):

        update_frontend_metrics()

        # Verifica se .labels().set() foi chamado com média correta
        assert mock_gauge.labels.call_count >= 4
        assert mock_gauge.labels.return_value.set.call_count >= 4

    mock_client.close.assert_called_once()


def test_update_frontend_metrics_with_exception():
    mock_db = MagicMock()
    mock_db.metrics.find.side_effect = Exception("erro de leitura")
    mock_client = MagicMock()

    with patch(
        "app.services.metrics.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        update_frontend_metrics()

    mock_client.close.assert_called_once()
