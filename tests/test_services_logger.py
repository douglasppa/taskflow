from unittest.mock import patch, MagicMock
from app.services.logger import log_event
from datetime import datetime, timezone


def test_log_event_writes_to_mongodb():
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_logs_collection = MagicMock()

    # Configura hierarquia: client[db].logs.insert_one
    mock_client.__getitem__.return_value = mock_db
    mock_db.logs = mock_logs_collection

    with patch(
        "app.services.logger.MongoClient", return_value=mock_client
    ) as mock_mongo:
        user_id = 42
        action = "created"
        data = {"field": "value"}

        log_event(user_id, action, data)

        # Valida se o MongoClient foi chamado com a URL do settings
        mock_mongo.assert_called_once()

        # Valida se insert_one foi chamado com os campos certos
        args, _ = mock_logs_collection.insert_one.call_args
        inserted_log = args[0]

        assert inserted_log["user_id"] == user_id
        assert inserted_log["action"] == action
        assert inserted_log["data"] == data
        assert isinstance(inserted_log["timestamp"], datetime)
        assert inserted_log["timestamp"].tzinfo == timezone.utc

        # Valida se client foi fechado
        mock_client.close.assert_called_once()
