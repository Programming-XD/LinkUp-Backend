from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio
import logging

loadMsg_bp = Blueprint('loadMsg', __name__)
user = User()
message = Message()

@loadMsg_bp.websocket('/ws/loadMsg/')
async def loadMsg():
  try:
    ws = websocket
    data = json.loads(await websocket.receive())
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
    await ws.send(json.dumps({"info": "Start listening for new messages!"}))
    while True:
      chatIdJson = json.loads(await websocket.receive())
      chat_id = str(chatIdJson.get('chat_id'))
      if chat_id and chat_id.isdigit():
        chat_id = int(chat_id)
        messages = await message.load_chat(user_id=user_id, session=session, chat_id=chat_id)
        if old_msg != messages:
          if isinstance(messages, str):
            await websocket.send(json.dumps({'error': messages}))
          else:
            await websocket.send(json.dumps({'data': messages}))
            logging.warn(messages)
            old_msg = messages
          logging.info("Sent a incoming msg notification!")
        await asyncio.sleep(0.3)
      else:
        await websocket.send(json.dumps({'error': 'chat_id required'}))
        return await websocket.close(code=1002)
  except Exception as e:
    logging.error(str(e))
    await websocket.send(json.dumps({'error': str(e)}))
    await websocket.close(code=1002)
    
    
# You may don't accept me now but i will never give up #
