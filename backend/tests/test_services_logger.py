from unittest.mock import patch, MagicMock
from app.services.logger import log_event
from datetime import datetime, timezone


def test_log_event_writes_to_mongodb():
    mock_db = MagicMock()
    mock_logs_collection = MagicMock()
    mock_client = MagicMock()

    mock_db.logs = mock_logs_collection

    with patch(
        "app.services.logger.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        user_id = 42
        action = "created"
        data = {"field": "value"}

        log_event(user_id, action, data)

        # Verifica se insert_one foi chamado com os dados corretos
        args, _ = mock_logs_collection.insert_one.call_args
        inserted_log = args[0]

        assert inserted_log["user_id"] == user_id
        assert inserted_log["action"] == action
        assert inserted_log["data"] == data
        assert isinstance(inserted_log["timestamp"], datetime)
        assert inserted_log["timestamp"].tzinfo == timezone.utc

        mock_client.close.assert_called_once()


def test_log_event_handles_insert_exception():
    mock_db = MagicMock()
    mock_logs_collection = MagicMock()
    mock_logs_collection.insert_one.side_effect = Exception("insert error")
    mock_db.logs = mock_logs_collection
    mock_client = MagicMock()

    with patch(
        "app.services.logger.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        # Deve rodar sem levantar erro
        log_event(1, "fail_test", {"data": "test"})


def test_log_event_handles_client_close_exception():
    mock_db = MagicMock()
    mock_logs_collection = MagicMock()
    mock_db.logs = mock_logs_collection

    mock_client = MagicMock()
    mock_client.close.side_effect = Exception("close error")

    with patch(
        "app.services.logger.get_sync_mongo_db", return_value=(mock_db, mock_client)
    ):
        log_event(1, "close_fail", {"data": "test"})
