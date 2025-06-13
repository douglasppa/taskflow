from datetime import datetime
from app.db.mongo import mongo_db

async def log_event(user_id: int, action: str, data: dict):
    log = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow(),
        "data": data
    }
    await mongo_db.logs.insert_one(log)