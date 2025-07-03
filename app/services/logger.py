from datetime import datetime, timezone
from app.db.mongo import get_sync_mongo_db


def log_event(user_id: int, action: str, data: dict):
    db, client = get_sync_mongo_db()

    log = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.now(timezone.utc),
        "data": data,
    }
    db.logs.insert_one(log)
    client.close()
