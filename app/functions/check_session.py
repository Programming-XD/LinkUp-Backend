from app import app
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

check_session_bp = Blueprint('check_session', __name__)
user = User()

@app.route('/check_session/', methods=['POST'])
async def check_session():
    data = await request.get_json()
    session = data.get('session')
    if not session:
        return jsonify({"error": "Where is session?"}), 400
    user_id = session.split('@')[0]
    if not user_id.isdigit():
        return jsonify({"error": "INVALID USER ID"}), 400
    user_id = int(user_id)
    check = await user.session(user_id=user_id, session=session, create_or_delete='chk')
    if check == 'INVALID USER':
        return jsonify({"error": "INVALID USER"}), 400
    elif check == "WRONG":
        return jsonify({"error": "Session doesn't match"}), 400
    elif check == "Same":
      return jsonify({"success": check}), 200
    else:
      return jsonify({"error": check}), 400
    
