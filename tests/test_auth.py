# tests/test_auth.py
import pytest

def test_register_and_login(client):
    register_data = {
        "email": "test@example.com",
        "hashed_password": "test123"
    }
    # Register user
    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 201

    # Login user
    response = client.post("/api/v1/auth/login", json=register_data)
    assert response.status_code == 200
    assert "access_token" in response.json()