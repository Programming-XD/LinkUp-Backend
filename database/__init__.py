import os
import config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_DB_URL = os.environ.get("MONGO_DB_URL") or config.MONGO_DB_URL
DATABASE = AsyncIOMotorClient(MONGO_DB_URL)["LinkUp"]

db, mdb = DATABASE["main"], DATABASE["message"]