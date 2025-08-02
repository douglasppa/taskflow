import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, Mock
from app.api.v1.routes_metrics import router as metrics_router
from fastapi import HTTPException

# Monta app de teste
app = FastAPI()
app.include_router(metrics_router, prefix="/api/v1")


@pytest.mark.asyncio
async def test_receive_metric_success():
    payload = {
        "name": "LCP",
        "value": 1234.56,
        "delta": 50,
        "id": "metric-id-123",
        "rating": "good",
        "navigationType": "navigate",
        "timestamp": "2025-07-31T13:28:32.797Z",
    }

    with patch("app.api.v1.routes_metrics.save_metric", new_callable=Mock) as mock_save:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/metrics", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_save.assert_called_once_with(payload)


@pytest.mark.asyncio
async def test_receive_metric_failure():
    payload = {
        "name": "CLS",
        "value": 0.2,
        "delta": 0.01,
        "id": "cls-id",
        "rating": "poor",
        "navigationType": "reload",
        "timestamp": "2025-07-31T13:40:00.000Z",
    }

    def failing_save_metric(_):
        raise Exception("falha simulada")

    with patch(
        "app.api.v1.routes_metrics.save_metric", side_effect=failing_save_metric
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/metrics", json=payload)

    assert response.status_code == 500
    assert "erro" in response.text.lower()


@pytest.mark.asyncio
async def test_receive_metric_http_exception():
    payload = {
        "name": "INP",
        "value": 300,
        "delta": 30,
        "id": "inp-id",
        "rating": "needs-improvement",
        "navigationType": "navigate",
        "timestamp": "2025-07-31T13:50:00.000Z",
    }

    def http_exception_save_metric(_):
        raise HTTPException(status_code=400, detail="Requisição inválida")

    with patch(
        "app.api.v1.routes_metrics.save_metric", side_effect=http_exception_save_metric
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/metrics", json=payload)

    assert response.status_code == 400
    assert "inválida" in response.text.lower()
