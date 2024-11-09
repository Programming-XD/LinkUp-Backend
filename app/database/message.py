from app import DATABASE
from datetime import datetime
from uuid import uuid4
from app.database.user import User

db = DATABASE['messages']

class Message:
    async def send(self, to, sender, text, session):
        user = User()
        
        sender_data = await user.get_user_details(sender)
        receiver_data = await user.get_user_details(to)
        
        if not sender_data:
            return "SENDER INVALID"
        if not receiver_data:
            return "RECEIVER INVALID"
        
        session_string = sender_data.get("session")
        if session != session_string:
            return "INVALID SESSION"
        
        message_id = str(uuid4())
        timestamp = datetime.now()
        sender_chat_data = {
            "to": to,
            "message_id": message_id,
            "text": text,
            "timestamp": timestamp,
            "seen": False
        }
        receiver_chat_data = {
            "from": sender,
            "message_id": message_id,
            "text": text,
            "timestamp": timestamp,
            "seen": False
        }
        
        await user.add_chat(sender, sender_chat_data)
        await user.add_chat(to, receiver_chat_data)
        
        return "Message sent"

    async def receive(self, username, session, old_message=0):
        user = User()
        
        user_data = await user.get_user_details(username)
        if not user_data:
            return "INVALID USER"
        
        if session != user_data.get("session"):
            return "INVALID SESSION"

        user_chats = user_data.get("chats", [])
        if not user_chats:
            return "No chats found"
        
        user_chats.sort(key=lambda x: x["timestamp"], reverse=True)

        limit = old_message if old_message > 0 else 100
        latest_messages = user_chats[:limit]

        return latest_messages
