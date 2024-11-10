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

        if not sender_data or not receiver_data:
            return "INVALID USER"
        if session != sender_data.get("session"):
            return "INVALID SESSION"

        message_id = str(uuid4())
        timestamp = datetime.now()
        
        sender_chat_data = {"to": to, "message_id": message_id, "text": text, "timestamp": timestamp, "seen": False}
        receiver_chat_data = {"from": sender, "message_id": message_id, "text": text, "timestamp": timestamp, "seen": False}
        
        await user.add_chat(sender, sender_chat_data)
        await user.add_chat(to, receiver_chat_data)
        return "Message sent"

    async def receive_new_messages(self, username, session):
        user = User()
        user_data = await user.get_user_details(username)

        if not user_data or session != user_data.get("session"):
            return "INVALID USER OR SESSION"

        unseen_messages = sorted(
            [chat for chat in user_data.get("chats", []) if not chat.get("seen", False)],
            key=lambda x: x["timestamp"],
            reverse=True
        )
        return unseen_messages[:1000]

    async def load_chat(self, chat_username, username, session, count=20):
        user = User()
        user_data = await user.get_user_details(username)

        if not user_data or session != user_data.get("session"):
            return "INVALID USER OR SESSION"
        
        chat_with_user = sorted(
            [chat for chat in user_data.get("chats", []) if chat.get("to") == chat_username or chat.get("from") == chat_username],
            key=lambda x: x["timestamp"],
            reverse=True
        )[:count]

        for chat in chat_with_user:
            chat["seen"] = True
        
        await self.update_chats(username, chat_with_user)
        return chat_with_user

    async def update_chats(self, username, updated_chat_data):
        user = User()
        await db.update_one({"_id": username}, {"$set": {"chats": updated_chat_data}})
        return "Chats updated successfully"
