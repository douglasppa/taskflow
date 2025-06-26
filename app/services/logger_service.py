from datetime import datetime
from pymongo import MongoClient
from app.core.config import settings


def log_event(user_id: int, action: str, data: dict):
    client = MongoClient(settings.MONGO_URL)
    db = client[settings.MONGO_DB_NAME]

    log = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow(),
        "data": data,
    }
    db.logs.insert_one(log)
    client.close()
