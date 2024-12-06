from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio
import logging

sendMessage_bp = Blueprint('sendMessage', __name__)
user = User()
message = Message()

@sendMessage_bp.websocket('/ws/sendMessage/')
async def sendMessage():
  try:
    print('hi')
  except Exception as e:
    print('oh')
