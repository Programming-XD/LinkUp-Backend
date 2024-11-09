from app import DATABASE
from datetime import datetime
from app.database.user import *

db = DATABASE['message']

class Message:
    async def send(to, sender, text, session):
        user = user()
        if await user.get_user_details(sender, True):
            if await user.get_user_details(to, True):
                session_string = await user.get_user_details(sender)['session']
                if session == session_string:
                    ?
                else:
                    return 'INVALID SESSION'
            else:
                return 'RECEIVER INVALID'
        else:
            return 'SENDER INVALID'
        
