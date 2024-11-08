from app import DATABASE


db = DATABASE['User']

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
    async def sign_up(self, name, username, password):
        list_users = await self.get_users()
        if username in list_users:
            return 'User exists'
        if len(password) >= 10:
            return 'Password too big'
        if len(password) <= 8:
            return 'Password too small'
        await db.insert_one({"_id": username, "name": name, "profile_picture": "https://i.imgur.com/juKF4kK.jpeg", "password": password})
        await db.update_one({"_id": 1}, {"$addToSet": {"users": username}}, upsert=True)
        return "success: sessionotazuki"
    async def login(self, username, password, session=None):
        if session:
            nothing
        else:
            if not await self.get_user_details(username, True):
                return 'INVALID USER'
            else:
                
