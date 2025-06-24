from datetime import datetime
from pymongo import MongoClient
import os

def log_event(user_id: int, action: str, data: dict):
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_db:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "taskflow")

    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]

    log = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow(),
        "data": data
    }
    db.logs.insert_one(log)
    client.close()