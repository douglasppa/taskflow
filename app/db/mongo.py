from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_db:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "taskflow")

client = AsyncIOMotorClient(MONGO_URL)
mongo_db = client[MONGO_DB_NAME]