from app import app
from app.database.message import Message
from app.database.user import User
from quart import request, jsonify, Blueprint

message_bp = Blueprint('message', __name__)
user = User()
message = Message()

@app.route('/send_message/', methods=['POST'])
async def send_message():
    data = await request.get_json()
    to, text, session = data.get('to'), data.get('text'), data.get('session')
    if not all([to, text, session]):
        return jsonify({"error": "All fields are required!"}), 400

    username = session.split('@')[0]
    result = await message.send(to=to, sender=username, text=text, session=session)
    status_code = 200 if result == 'Message sent' else 400
    return jsonify({"success" if status_code == 200 else "error": result}), status_code

@app.route('/receive_messages/', methods=['POST'])
async def receive_messages():
    data = await request.get_json()
    session = data.get('session')
    if not session:
        return jsonify({"error": "Session is required"}), 400

    username = session.split('@')[0]
    user_details = await user.get_user_details(username)
    if not user_details or user_details.get('session') != session:
        return jsonify({"error": "Invalid session"}), 400

    messages = await message.receive_new_messages(username=username, session=session)
    return jsonify({"messages": messages}), 200 if not isinstance(messages, str) else jsonify({"error": messages}), 400

@app.route('/load_chat/', methods=['POST'])
async def load_chat():
    data = await request.get_json()
    session, chat_username, count = data.get('session'), data.get('chat_username'), data.get('count', 20)
    if not session or not chat_username:
        return jsonify({"error": "Session and chat username are required!"}), 400

    username = session.split('@')[0]
    user_details = await user.get_user_details(username)
    if not user_details or user_details.get('session') != session:
        return jsonify({"error": "Invalid session"}), 400

    chat_data = await message.load_chat(chat_username=chat_username, username=username, session=session, count=count)
    if isinstance(chat_data, str):
        return jsonify({"error": chat_data}), 400
    return jsonify({"chat_data": chat_data}), 200
