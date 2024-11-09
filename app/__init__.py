from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
from variables import *
import os
from flask import Flask
from app.functions.login import login

# REGISTER
app.register_blueprint(login)

# LOGGING
logging.basicConfig(
    format="[LinkUp-Backend] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)


# VARIABLES
MONGO_DB_URL = os.environ.get("MONGO_DB_URL") or VAR_MONGO_DB_URL


# DATABASE
logging.info('Starting database...')
DATABASE = AsyncIOMotorClient(MONGO_DB_URL)["LinkUp"]
app = Flask(__name__)
