from app import app
import logging 
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

userinfo_bp = Blueprint('userinfo', __name__)
user = User()

@app.route('/userinfo/', methods=['POST'])
async def userinfo():
  data = await request.get_json()
  session = data.get('session') or None
  chat_id = str(data.get('chat_id')) or None
  user_id = str(session.split('@')[0]) 
  if not session:
    return jsonify({"error": "Where is session"}), 400
  elif not chat_id:
    return jsonify({"error": "Hmm, ig you finding your gf id isn't?"}), 400
  elif chat_id == user_id:
    return jsonify({'error': "Why user_id and chat_id is same???"}), 400
  
  if chat_id.isdigit() and user_id.isdigit():
    chat_id = int(chat_id)
    user_id = int(user_id)
  else:
    return jsonify({"error": "Invalid chat_id/session"}), 400
  session_stats = await user.session(user_id=user_id, create_or_delete="chk", session=session)
  if session_stats == "Same":
    try:
      details = await user.get_user_details(chat_id)
      if details:
        output = {
          'profile_picture': details.get('profile_picture'),
          'name': details.get('name'),
          'username': details.get('username')
        }
        return jsonify({"output": output}), 200
      else:
        return jsonify({"error": f"Invalid chat id"}), 400
    except Exception as e:
      logging.error(f'Error while fetching, details of user: {user_id}, Error: {e}')
      return jsonify({"error": f'Error while fetching, details of user: {user_id}, Error: {e}'}), 400
  elif session_stats == "WRONG":
    return jsonify({"error": f"Wrong session"}), 400
  else:
    return jsonify({"error": f"Invalid session/User & {session_stats}"}), 400
