from unittest.mock import patch
from app.workers import logging_tasks


def test_test_task(capsys):
    result = logging_tasks.test_task()

    assert result == "Hello from Celery"
    captured = capsys.readouterr()
    assert "Celery está funcionando!" in captured.out


def test_log_event_calls_sync_log_event():
    user_id = "123"
    action = "TEST_ACTION"
    data = {"key": "value"}

    with patch("app.workers.logging_tasks.sync_log_event") as mock_sync:
        logging_tasks.log_event(user_id, action, data)

        mock_sync.assert_called_once_with(user_id=user_id, action=action, data=data)
