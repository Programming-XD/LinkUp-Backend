from app import DATABASE
from datetime import datetime
from uuid import uuid4
from app.database.user import User
from app.database.user import db as udb
import pytz
from datetime import datetime

async def get_time():
    utc_now = datetime.now(pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = utc_now.astimezone(ist)
    return ist_time.isoformat()

db = DATABASE['message']


class Message:
    async def send(self, to, sender, text, session):
        user = User()
        sender_data = await user.get_user_details(sender)
        receiver_data = await user.get_user_details(to)

        if not sender_data:
            return "INVALID USER"
        if not receiver_data:
            return "INVALID RECIPIENT"
        if session != sender_data.get("session"):
            return "INVALID SESSION"
        if to == sender:
            return "You can't send message to yourself!"

        message_id = str(uuid4())
        timestamp = await get_time()
        
        sender_chat_data = {"to": to, "message_id": message_id, "text": text, "timestamp": timestamp, "seen": False}
        receiver_chat_data = {"from": sender, "message_id": message_id, "text": text, "timestamp": timestamp, "seen": False}
        
        await user.add_chat(sender, sender_chat_data, to)
        await user.add_chat(to, receiver_chat_data, sender)
        return "Message sent"

    async def receive_new_messages(self, user_id, session):
        user = User()
        user_data = await user.get_user_details(user_id)

        if not user_data or session != user_data.get("session"):
            return "INVALID USER OR SESSION"

        valid_chats = [
            chat for chat in user_data.get("chats", [])
            if isinstance(chat, dict) and "to" not in chat
        ]

        unseen_messages = sorted(
            [chat for chat in valid_chats if not chat.get("seen")],
            key=lambda x: datetime.fromisoformat(str(x["timestamp"])) if isinstance(x["timestamp"], str) else datetime.min,
            reverse=True
        )
        return unseen_messages[:100000]

    async def load_chat(self, chat_id, user_id, session, count=20):
        user = User()
        user_data = await user.get_user_details(user_id)

        if not user_data or session != user_data.get("session"):
            return "INVALID USER OR SESSION"

        valid_chats = [
            chat for chat in user_data.get("chats", [])
            if isinstance(chat, dict)
        ]
        
        chat_with_user = sorted(
            [chat for chat in valid_chats if chat.get("to") == chat_id or chat.get("from") == chat_id],
            key=lambda x: datetime.fromisoformat(str(x["timestamp"])) if isinstance(x["timestamp"], str) else datetime.min,
            reverse=True
        )[:count]
        
        for chat in chat_with_user:
            chat["seen"] = True
        
        await self.update_chats(user_id, chat_with_user)
        return chat_with_user

    async def update_chats(self, user_id, updated_chat_data):
        user = User()
        if updated_chat_data:
            await udb.update_one({"_id": user_id}, {"$set": {"chats": updated_chat_data}})
            return "Chats updated successfully"
