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
    data = json.loads(await websocket.receive())
    session = data.get('session')
    user_id = str(session.split('@')[0])
    if not session:
      await websocket.send(json.dumps({'error': 'Session required'}))
      return await websocket.close(code=1002)
    elif not user_id.isdigit():
      await websocket.send(json.dumps({'error': 'Invalid session'}))
      return await websocket.close(code=1002)
    try:
      user_id = int(user_id)
    except ValueError:
      await websocket.send(json.dumps({'error': f"The {user_id} (user_id) in session are invalid. check your session!"}))
      return await websocket.close(code=1002)
    user_details = await user.get_user_details(user_id)
    if not user_details or user_details.get('session') != session:
      await websocket.send(json.dumps({"error": "Invalid session or user"}))
      return await websocket.close(code=1002)
    while True:
      msg_data = json.loads(await websocket.receive())
      if msg_data:
        to = msg_data.get('to')
        message = msg_data.get('message')
        if not to:
          await ws.send(json.dumps({'error': "'to' id is required"}))
          return await ws.close(code=1002)
        elif not message:
          await ws.send(json.dumps({'error': "'message' is required"}))
          return await ws.close(code=1002)
        
  except Exception as e:
    print('oh')
