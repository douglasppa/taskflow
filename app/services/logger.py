from datetime import datetime, timezone
from app.db.mongo import get_sync_mongo_db
from app.core.logger import log, LogLevel


def log_event(user_id: int, action: str, data: dict):
    try:
        db, client = get_sync_mongo_db()

        log_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now(timezone.utc),
            "data": data,
        }
        db.logs.insert_one(log_data)
    except Exception as e:
        log(f"Error saving log to MongoDB: {e}", level=LogLevel.ERROR)
    finally:
        try:
            client.close()
        except Exception:
            pass
