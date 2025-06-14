# tests/test_task.py
import pytest
from http import HTTPStatus

def test_task_flow(client):
    # Ensure the user is registered and logged in
    data = {"email": "test@example.com", "password": "test123"}
    client.post("/api/v1/auth/register", json=data)
    login_response = client.post("/api/v1/auth/login", json=data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a new task
    create_response = client.post("/api/v1/tasks/", json={"title": "Nova tarefa", "description": "Descrição da tarefa"}, headers=headers)
    assert create_response.status_code == HTTPStatus.CREATED
    assert "id" in create_response.json()
    assert create_response.json()["title"] == "Nova tarefa"
    assert create_response.json()["description"] == "Descrição da tarefa"
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Tarefa atualizada",
        "description": "Descrição atualizada"
    }
    update_response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers)
    assert update_response.status_code == HTTPStatus.OK
    assert update_response.json()["title"] == update_data["title"]
    assert update_response.json()["description"] == update_data["description"]

    # List the task
    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == update_data["title"]
    assert get_response.json()["description"] == update_data["description"]

    # Delete the task
    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == HTTPStatus.NO_CONTENT