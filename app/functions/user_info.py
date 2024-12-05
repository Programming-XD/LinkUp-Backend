from app import app
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

userinfo_bp = Blueprint('userinfo', __name__)
user = User()

@app.route('/userinfo/', methods=['POST'])
async def userinfo():
  data = await request.get_json()
  session = data.get('session') or None
  if not session:
    return jsonify({"error": "Where is session"}), 400
  user_id = session.split('@')[0]
  if user_id.isdigit():
    user_id = int(user_id)
  else:
    return jsonify({"error": "Invalid session"}), 400
  session_stats = await user.session(user_id=user_id, create_or_delete="chk", session=session)
  if session_stats == "Same":
    details = await user.get_user_details(user_id)
    output = {
      'profile_picture': details['profile_picture'],
      'name': details['name'],
      'username': details['username']
    }
    return jsonify({"output": output}), 200
  elif session_stats == "WRONG":
    return jsonify({"error": "Invalid session"}), 400
  else:
    return jsonify({"error": "Invalid session/User"}), 400
