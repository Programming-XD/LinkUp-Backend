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
        return jsonify({"error": "Where is session?"}), 400
    get_chats = await user.get_chats(session)
    if get_chats == 'INVALID SESSION':
        return jsonify({"error": "INVALID SESSION"}), 400
    elif get_chats == "INVALID USER":
        return jsonify({"error": "INVALID USER"}), 400
    return jsonify({"chats": get_chats}), 200
    
