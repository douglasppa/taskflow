# tests/test_healthcheck.py
import pytest
from http import HTTPStatus

def test_healthcheck(client):
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}