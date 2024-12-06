from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio
import logging

message_unseen_bp = Blueprint('message_unseen', __name__)
user = User()
message = Message()

@message_unseen_bp.websocket('/ws/msguns/')
async def message_unseen():
  try:
    ws = websocket
    data = json.loads(await websocket.receive())
    logging.info('someone coming: %s', data)
    session = data.get('session')
    user_id = str(session.split('@')[0])
    if not session:
      await websocket.send(json.dumps({'error': 'Session required'}))
      await websocket.close(code=1002)
      return 
    elif not user_id.isdigit():
      await websocket.send(json.dumps({'error': 'Invalid session'}))
      await websocket.close(code=1002)
      return
    try:
      user_id = int(user_id)
    except ValueError:
      await websocket.send(json.dumps({'error': f"The {user_id} (user_id) in session are invalid. check your session!"}))
      await websocket.close(code=1002)
      return
    user_details = await user.get_user_details(user_id)
    if not user_details or user_details.get('session') != session:
      await websocket.send(json.dumps({"error": "Invalid session or user"}))
      await websocket.close(code=1002)
      return 
    old_msg = []
    await ws.send("Start listening for new messages!")
    while True:
      messages = await message.receive_new_messages(user_id=user_id, session=session)
      if old_msg != messages:
        if isinstance(messages, str):
          await websocket.send(json.dumps({'error': messages}))
        else:
          await websocket.send(json.dumps(messages))
          old_msg = messages
        logging.info("Sent a incoming msg notification!")
      await asyncio.sleep(0.3)
  except Exception as e:
    logging.error(str(e))
    await websocket.send(json.dumps({'error': str(e)}))
    await websocket.close(code=1002)
    
    
