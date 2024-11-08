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
    async def sign_up(self, name, username, password):
        list_users = await self.get_users()
        if username in list_users:
            return 'User exists'
        if len(password) >= 10:
            return 'Password too big'
        await db.insert_one({"_id": username, "name": name, "profile_picture": "https://i.imgur.com/juKF4kK.jpeg", "password": password})
        await db.update_one({"_id": 1}, {"$addToSet": {"users": user_id}}, upsert=True)
        return "success"
