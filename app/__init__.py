from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
import config
import os
from quart import Quart
from quart_cors import cors

# LOGGING
logging.basicConfig(
  format="[LinkUp-Backend] %(name)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

MONGO_DB_URL = os.environ.get("MONGO_DB_URL") or config.MONGO_DB_URL

# DATABASE
DATABASE = AsyncIOMotorClient(MONGO_DB_URL)["LinkUp"]
app = Quart(__name__)