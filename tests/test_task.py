# tests/test_task.py
import pytest

def test_create_task(client):
    data = {"email": "test@example.com", "hashed_password": "test123"}
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201

    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.json()