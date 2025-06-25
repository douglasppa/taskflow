# tests/test_healthcheck.py
from http import HTTPStatus


def test_liveness(client):
    response = client.get("/api/v1/health/live")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "alive"}


def test_readiness(client):
    response = client.get("/api/v1/health/ready")
    assert response.status_code == HTTPStatus.OK
