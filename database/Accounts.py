from . import *
from errors import *
import random

AccountTypes = ['user', 'support', 'bot']
class Accounts:
  async def new(
    self,
    name,
    type = 'user',
    username = None,
    password_hash = None,
  ):
    if type not in AccountTypes:
      return {"code": 404, "message": "Account type is invalid."}
    elif type == 'user':
      if not password_hash:
        return {"code": 400, "message": "Password hash is missing."}
      elif not isinstance(username, str) or not isinstance(name, str), not isinstance(password_hash, str):
        return {"code": 500, "message": "Internal issues probably, the args of Accounts.new is not str."}
      elif len(username) > 14 or len(username) < 4:
        return {"code": 422, "message": "Size of the username is invalid, usernames should be 4 to 14 in char."}
      elif len(name) > 24 or len(name) < 2:
        return {"code": 422, "message": "Size of the user's name is invalid, user's name should be 4 to 24 in char."}
      # i should add a logic to check password length!
      user_id = random.randint(1000000000, 9999999999)
      await db.update_one({"_id": f"account-{user_id}"}, {"$set": {"name": name, "username": username, "user_id": user_id, "type": type, "password_hash": password_hash}}, upsert=True)
      return True
    else:
      return {"code": 501, "message": f"{type} will be added in future."}