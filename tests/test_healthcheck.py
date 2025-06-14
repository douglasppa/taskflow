# tests/test_healthcheck.py
import pytest

def test_healthcheck(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}