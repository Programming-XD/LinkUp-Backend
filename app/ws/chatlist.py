from app import *
from quart import *
from app.database.message import Message
from app.database.user import User
import json
import asyncio
import logging

chatlist_bp = Blueprint('chatlistws', __name__)
user = User()

@chatlist_bp.websocket('/ws/chatlist/')
async def chatlist():
    try:
        w = websocket 
        data = json.loads(await websocket.receive())
        session = data.get('session')
        if not session:
            await w.send(json.dumps({"error": "Where is session?"}))
            return await w.close(code=1002)
        old_chatlist = []
        while True:
            get_chats = await user.get_chats(session)
            if get_chats == 'INVALID SESSION':
                await w.send(json.dumps({"error": "INVALID SESSION"}))
                return await w.close(code=1002)
            elif get_chats == "INVALID USER":
                await w.send(json.dumps({"error": "INVALID USER"}))
                return await w.close(code=1002)
            if get_chats != old_chatlist:
                await w.send(json.dumps({"chats": get_chats}))
                old_chatlist = get_chats
            await asyncio.sleep(0.3)
    except Exception as e:
        logging.error(str(e))
        await websocket.send(str(e))
        await websocket.close(code=1002)

