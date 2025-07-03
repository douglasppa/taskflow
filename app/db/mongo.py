from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.core.config import settings

# Cliente assíncrono global (FastAPI)
_async_client = AsyncIOMotorClient(settings.MONGO_URL)


def get_mongo_db():
    """
    Retorna o banco Mongo assíncrono para uso com `motor` (FastAPI).
    Uso:
        db = get_mongo_db()
        await db.collection.find_one(...)
    """
    return _async_client[settings.MONGO_DB_NAME]


def get_sync_mongo_db():
    """
    Retorna uma nova instância de cliente e banco Mongo síncrono (pymongo).
    É responsabilidade do chamador fechar o client.
    Uso:
        db, client = get_sync_mongo_db()
        db.collection.insert_one(...)
        client.close()
    """
    client = MongoClient(settings.MONGO_URL)
    return client[settings.MONGO_DB_NAME], client
