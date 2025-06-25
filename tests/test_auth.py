# tests/test_auth.py
from http import HTTPStatus

def test_register_and_login(client):
    data = {"email": "test@example.com", "password": "test123"}

    # Register user
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code in (HTTPStatus.CREATED, HTTPStatus.CONFLICT)

    # Login user
    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()