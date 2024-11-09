from app import app
from app.database.message import *
from app.database.user import *
from quart import request, jsonify, Blueprint

message_bp = Blueprint('message', __name__)
user = User()
message = Message()

@app.route('/send_message/', methods=['POST'])
async def send_message():
    data = await request.get_json()
    to = data.get('to')
    text = data.get('text')
    session = data.get('session')
    username = session.split('@')[0]
    if not to or not text or not session:
        return jsonify({"error": "All fields are required!"}), 400
    result = await message.send(to=to, sender=username, text=text, session=session)
    if result == 'Message sent':
        return jsonify({"success": result}), 200
    return jsonify({"error": result}), 400

@app.route('/receive_messages/', methods=['POST'])
async def receive_messages():
    data = await request.get_json()
    session = data.get('session')
    old_message = data.get('old_message', 0)

    username = session.split('@')[0]
    user_details = await user.get_user_details(username)
    if not user_details or user_details.get('session') != session:
        return jsonify({"error": "Invalid session"}), 400

    messages = await message.receive(session=session, old_message=old_message)
    if isinstance(messages, str):
        return jsonify({"error": messages}), 400
    return jsonify({"messages": messages}), 200
