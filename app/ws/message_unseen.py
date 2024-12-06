from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio

message_unseen_bp = Blueprint('message_unseen', __name__)
user = User()
message = Message()

@message_unseen_bp.websocket('/ws/msguns/')
async def test():
  data = json.loads(await websocket.receive())
  session = data.get('session')
  if not session:
    await websocket.send(json.dumps({'error': 'Session required'}))
    return await websocket.close()
  user_id = str(session.split('@')[0])
  if not user_id.isdigit():
    await websocket.send(json.dumps({'error': 'Invalid session'}))
    return await websocket.close()
  user_id = int(user_id)
  user_details = await user.get_user_details(user_id)
  if not user_details or user_details.get('session') != session:
    await websocket.send(json.dumps({"error": "Invalid session or user"}))
    return await websocket.close()
  old_msg = {}
  while True:
    messages = await message.receive_new_messages(user_id=user_id, session=session)
    if old_msg != messages:
      if isinstance(messages, str):
        await websocket.send(json.dumps({"error": messages})), 400
      else:
        await websocket.send(json.dumps({"messages": messages})), 200
    await asyncio.sleep(0.3)
    
    
