from app import app
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

check_session = Blueprint('check_session', __name__)
user = User()

@app.route('/check_session/', methods=['POST'])
async def chatlist():
    data = await request.get_json()
    session = data.get('session')
    if not session:
        return jsonify({"error": "Where is session?"})
    user_id = int(session.split('@')[0])
    check = await user.session(user_id=user_id, session=session, create_or_delete='chk')
    if check == 'INVALID USER':
        return jsonify({"error": "INVALID USER"}), 400
    elif check == "WRONG":
        return jsonify({"error": "Session doesn't match"}), 400
    elif check == "Same":
      return jsonify({"success": check}), 200
    else:
      return jsonify({"error": check}), 400
    
