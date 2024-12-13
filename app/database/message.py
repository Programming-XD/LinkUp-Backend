from app import DATABASE
from datetime import datetime
from uuid import uuid4
from app.database.user import User
from app.database.user import db as udb
import pytz
import logging
from datetime import datetime

async def get_time():
    utc_now = datetime.now(pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = utc_now.astimezone(ist)
    return ist_time.isoformat()

db = DATABASE['messages']


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
        user_data = await user.get_user_details(user_id, True)
        user_info = await user.get_user_details(user_id, False)
        
        if not user_info or session != user_info.get("session"):
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

    async def load_chat(self, chat_id, user_id, session, count=50):
        user = User()
        user_data = await user.get_user_details(user_id, True)
        user_info = await user.get_user_details(user_id)

        if not user_info or session != user_info.get("session"):
            return "INVALID USER OR SESSION"

        valid_chats = user_data.get("chats", [])
        chat_with_user = sorted(
            [chat for chat in valid_chats if chat.get("to") == chat_id or chat.get("from") == chat_id],
            key=lambda x: datetime.fromisoformat(str(x["timestamp"])) if isinstance(x["timestamp"], str) else datetime.min,
            reverse=False
        )[:count]

        for chat in chat_with_user:
            chat["seen"] = True

        updated_chats = []
        chat_ids_updated = {chat["message_id"] for chat in chat_with_user}

        for chat in valid_chats:
            if chat["message_id"] in chat_ids_updated:
                updated_chats.append(next(c for c in chat_with_user if c["message_id"] == chat["message_id"]))
            else:
                updated_chats.append(chat)

        await self.update_chats(user_id, updated_chats)
        return chat_with_user

    async def update_chats(self, user_id, updated_chat_data):
        if not len(updated_chat_data) >= 1:
            return "why too short?"
        user = User()
        await db.update_one({"_id": user_id}, {"$set": {"chats": updated_chat_data}})
        return "Chats updated successfully"
