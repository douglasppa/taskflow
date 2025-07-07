from http import HTTPStatus
from unittest.mock import patch
from app.models.task import Task
import pytest


@pytest.fixture
def auth_headers(client):
    data = {"email": "test@example.com", "password": "test123"}
    client.post("/api/v1/auth/register", json=data)
    response = client.post("/api/v1/auth/login", json=data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ==============================================================================
# POST /tasks/
# ==============================================================================


def test_create_task(client, auth_headers):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Teste", "description": ""},
        headers=auth_headers,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert "id" in response.json()
    assert response.json()["title"] == "Teste"


def test_create_with_latency(client, auth_headers):
    with patch("app.api.v1.routes_task.settings.features.simulate_task_latency", True):
        with patch("app.services.task.create_task") as mock_create:
            mock_create.return_value = {
                "id": 1,
                "title": "Latente",
                "description": "",
                "owner_id": 1,
            }
            response = client.post(
                "/api/v1/tasks/",
                json={"title": "Latente", "description": ""},
                headers=auth_headers,
            )
            assert response.status_code == HTTPStatus.CREATED


# ==============================================================================
# GET /tasks/
# ==============================================================================


def test_list_tasks(client, auth_headers):
    response = client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


# ==============================================================================
# GET /tasks/{task_id}
# ==============================================================================


def test_get_task(client, auth_headers):
    create = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "description": ""},
        headers=auth_headers,
    )
    task_id = create.json()["id"]
    response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == task_id


def test_get_task_not_found(client, auth_headers):
    response = client.get("/api/v1/tasks/99999", headers=auth_headers)
    assert response.status_code == HTTPStatus.CONFLICT


# ==============================================================================
# PUT /tasks/{task_id}
# ==============================================================================


def test_update_task_success(client, auth_headers):
    create = client.post(
        "/api/v1/tasks/", json={"title": "Old", "description": ""}, headers=auth_headers
    )
    task_id = create.json()["id"]
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "New", "description": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "New"


def test_update_task_not_found(client, auth_headers):
    response = client.put(
        "/api/v1/tasks/99999",
        json={"title": "X", "description": "X"},
        headers=auth_headers,
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_task_other_user(client, auth_headers, db_session):
    task = Task(title="Outra", description="x", owner_id=999)
    db_session.add(task)
    db_session.commit()
    response = client.put(
        f"/api/v1/tasks/{task.id}",
        json={"title": "hack", "description": "tentativa"},
        headers=auth_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# DELETE /tasks/{task_id}
# ==============================================================================


def test_delete_task_success(client, auth_headers):
    create = client.post(
        "/api/v1/tasks/", json={"title": "Del", "description": ""}, headers=auth_headers
    )
    task_id = create.json()["id"]
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.OK)


def test_delete_task_not_found(client, auth_headers):
    response = client.delete("/api/v1/tasks/99999", headers=auth_headers)
    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_task_other_user(client, auth_headers, db_session):
    task = Task(title="Outro dono", description="x", owner_id=999)
    db_session.add(task)
    db_session.commit()
    response = client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_task_failure(client, auth_headers, db_session):
    task = Task(title="Deletável", description="", owner_id=1)
    db_session.add(task)
    db_session.commit()
    with patch("app.services.task.delete_task", return_value=False):
        response = client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


# ==============================================================================
# GET /tasks/summary
# ==============================================================================


def test_summary_disabled(client, auth_headers):
    with patch(
        "app.api.v1.routes_task.settings.features.enable_summary_endpoint", False
    ):
        response = client.get("/api/v1/tasks/summary", headers=auth_headers)
        assert response.status_code == HTTPStatus.NOT_FOUND


def test_summary_success(client, auth_headers):
    with patch(
        "app.api.v1.routes_task.settings.features.enable_summary_endpoint", True
    ):
        response = client.get("/api/v1/tasks/summary", headers=auth_headers)
        assert response.status_code == HTTPStatus.OK
        json = response.json()
        assert "user_id" in json
        assert "total_tasks" in json


def test_summary_internal_error(client, auth_headers):
    with patch(
        "app.api.v1.routes_task.settings.features.enable_summary_endpoint", True
    ):
        with patch("app.api.v1.routes_task.Task") as mock_task:
            # Força a query a lançar exceção
            mock_task.id.side_effect = Exception("DB error")

            response = client.get("/api/v1/tasks/summary", headers=auth_headers)
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json()["detail"] == "Failed to generate task summary"
