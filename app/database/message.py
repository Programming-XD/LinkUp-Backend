from app import DATABASE
from datetime import datetime
from uuid import uuid4
from app.database.user import User

db = DATABASE['messages']

class Message:
    async def send(self, to, sender, text, session):
        user = User()
        
        if await user.get_user_details(sender, True):
            if await user.get_user_details(to, True):
                session_string = await user.get_user_details(sender)['session']
                if session == session_string:
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
                else:
                    return "INVALID SESSION"
            else:
                return "RECEIVER INVALID"
        else:
            return "SENDER INVALID"

    async def receive(self, username, old_message=0):
        user = User()
        user_chats = await db.find_one({"_id": username})
        if not user_chats:
            return "No chats found"

        all_messages = []
        for chat in user_chats.get("chats", []):
            all_messages.append(chat)

        all_messages.sort(key=lambda x: x["timestamp"], reverse=True)

        limit = old_message if old_message > 0 else 100
        latest_messages = all_messages[:limit]

        for message in latest_messages:
            await self.update_seen_status(username, message["message_id"])

        return latest_messages

    async def update_seen_status(self, username, message_id):
        await db.update_one({"_id": username, "chats.message_id": message_id}, {"$set": {"chats.$.seen": True}})
