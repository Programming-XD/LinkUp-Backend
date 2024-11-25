from app import app
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

chatlist_bp = Blueprint('chatlist', __name__)
user = User()

@app.route('/chatlist/', methods=['POST'])
async def chatlist():
    data = await request.get_json()
    session = data.get('session')
    if not session:
        return jsonify({"error": "Where is session?"})
    user_info = await user.get_user_details(username)
    if user_info['session'] != session:
        return jsonify({"error": "Invalid session"}), 400
    elif not user_info:
        return jsonify({"error": "Invalid user"}), 400
    chats = user_info["chatlist"] or []
    return jsonify({"chats": chats}), 200
    
