from app import DATABASE
import secrets
from uuid import uuid4

db = DATABASE['user_data_beta']

class User:
    async def get_users(self):
        list_users = await db.find_one({"_id": 1})
        if not list_users:
            return []
        else:
            list_users = list_users.get("users", [])
            return list_users

    async def get_user_details(self, username, check_available=False):
        if check_available:
            user = await db.find_one({"_id": username})
            if not user:
                return False
            return True
        else:
            user = await db.find_one({"_id": username})
            if not user:
                return False
            return user

    async def session(self, username, password, create_or_delete='create'):
        if create_or_delete == 'create':
            if await self.get_user_details(username, True):
                session_string = secrets.token_hex(30)
                session_string = f"{username}@{session_string}"
                return session_string
            else:
                return 'INVALID USER'

    async def sign_up(self, name, username, password):
        list_users = await self.get_users()
        username = username.lower()
        if username in list_users:
            return 'User exists'
        if len(password) > 14:
            return 'Password too big'
        if len(password) <= 8:
            return 'Password too small'
        if len(username) > 14:
            return 'Username too big'
        if len(username) <= 3:
            return 'Username too small'
        if len(name) >= 16:
            return 'Name too big'
        if len(name) <= 3:
            return 'Name too small'
        await db.insert_one({"_id": username, "name": name, "profile_picture": "https://i.imgur.com/juKF4kK.jpeg", "password": password, "session": None, "chats": []})
        await db.update_one({"_id": 1}, {"$addToSet": {"users": username}}, upsert=True)
        session_string = await self.session(username, password)
        await db.update_one({"_id": username}, {"$set": {"session": session_string}}) 
        return f"success: {session_string}"

    async def login(self, username=None, password=None, session=None):
        username = username.lower()
        if session:
            get_user_details = await self.get_user_details(username)
            if '@' not in session:
                return 'INVALID SESSION FORMAT'
            username = session.split('@')[0]
            session_string = get_user_details['session']
            if session == session_string:
                return f"success: {session_string}"
            else:
                return 'INVALID SESSION'
        else:
            if not await self.get_user_details(username, True):
                return 'INVALID USER'
            else:
                get_user_details = await self.get_user_details(username)
                original_password = get_user_details['password']
                if original_password == password:
                    session_string = await self.session(username, password)
                    await db.update_one({"_id": username}, {"$set": {"session": session_string}})
                    return f"success: {session_string}"
                else:
                    return 'WRONG PASSWORD'

    async def add_chat(self, username, chat_data, chat_username):
        await db.update_one({"_id": username}, {"$push": {"chats": chat_data}}, upsert=True)
        chats = await self.get_user_details(username)
        chats = chats.get('chatlist') or []
        if chat_username not in chats:
            await db.update_one({"_id": username}, {"$addToSet": {"chatlist": chat_username}}, upsert=True)
        
