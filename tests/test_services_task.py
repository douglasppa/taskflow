from unittest.mock import patch
from app.services import task as task_service
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task


def make_fake_user():
    return {"sub": "123"}


def make_fake_task(id=1, title="Task 1", description="Desc", owner_id="123"):
    return Task(id=id, title=title, description=description, owner_id=owner_id)


# ==============================================================================
# create_task
# ==============================================================================


def test_create_task_success(db_session):
    user = make_fake_user()
    task_data = TaskCreate(title="Test", description="Desc")

    with patch("app.services.task.log_event.delay") as mock_log:
        result = task_service.create_task(db_session, task_data, user)

    assert result.id is not None
    assert result.title == "Test"
    mock_log.assert_called_once()


def test_create_task_with_log_error(db_session):
    user = make_fake_user()
    task_data = TaskCreate(title="Erro", description="Erro log")

    with patch(
        "app.services.task.log_event.delay", side_effect=Exception("fail")
    ) as mock_log:
        result = task_service.create_task(db_session, task_data, user)

    assert result.title == "Erro"
    mock_log.assert_called_once()


# ==============================================================================
# get_task
# ==============================================================================


def test_get_task_found(db_session):
    created = task_service.create_task(
        db_session, TaskCreate(title="Get", description=""), make_fake_user()
    )
    fetched = task_service.get_task(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_task_not_found(db_session):
    assert task_service.get_task(db_session, 9999) is None


# ==============================================================================
# list_tasks
# ==============================================================================


def test_list_tasks(db_session):
    task_service.create_task(
        db_session, TaskCreate(title="T1", description=""), make_fake_user()
    )
    task_service.create_task(
        db_session, TaskCreate(title="T2", description=""), make_fake_user()
    )

    result = task_service.list_tasks(db_session, skip=0, limit=10)
    assert isinstance(result, list)
    assert len(result) >= 2


# ==============================================================================
# update_task
# ==============================================================================


def test_update_task_success(db_session):
    user = make_fake_user()
    task = task_service.create_task(
        db_session, TaskCreate(title="Old", description="Old"), user
    )

    update_data = TaskUpdate(title="Updated")
    with patch("app.services.task.log_event.delay") as mock_log:
        updated = task_service.update_task(db_session, task.id, update_data, user)

    assert updated.title == "Updated"
    mock_log.assert_called_once()


def test_update_task_with_log_error(db_session):
    user = make_fake_user()
    task = task_service.create_task(
        db_session, TaskCreate(title="X", description="X"), user
    )

    update_data = TaskUpdate(description="Changed")
    with patch(
        "app.services.task.log_event.delay", side_effect=Exception("fail")
    ) as mock_log:
        updated = task_service.update_task(db_session, task.id, update_data, user)

    assert updated.description == "Changed"
    mock_log.assert_called_once()


# ==============================================================================
# delete_task
# ==============================================================================


def test_delete_task_success(db_session):
    user = make_fake_user()
    task = task_service.create_task(
        db_session, TaskCreate(title="Delete", description=""), user
    )

    with patch("app.services.task.log_event.delay") as mock_log:
        deleted = task_service.delete_task(db_session, task.id, user)

    assert deleted.id == task.id
    mock_log.assert_called_once()


def test_delete_task_with_log_error(db_session):
    user = make_fake_user()
    task = task_service.create_task(
        db_session, TaskCreate(title="Erro Delete", description=""), user
    )

    with patch(
        "app.services.task.log_event.delay", side_effect=Exception("fail")
    ) as mock_log:
        deleted = task_service.delete_task(db_session, task.id, user)

    assert deleted.id == task.id
    mock_log.assert_called_once()
