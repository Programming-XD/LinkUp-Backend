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
    to = int(to)
    
    if not all([to, text, session]):
        return jsonify({"error": "All fields are required!"}), 400

    user_id = int(session.split('@')[0])
    result = await message.send(to=to, sender=user_id, text=text, session=session)
    status_code = 200 if result == 'Message sent' else 400
    return jsonify({"success" if status_code == 200 else "error": result}), status_code

@app.route('/receive_messages/', methods=['POST'])
async def receive_messages():
    data = await request.get_json()
    session = data.get('session')
    
    if not session:
        return jsonify({"error": "Session is required"}), 400

    user_id = int(session.split('@')[0])
    user_details = await user.get_user_details(user_id)
    
    if not user_details or user_details.get('session') != session:
        return jsonify({"error": "Invalid session or user"}), 400

    messages = await message.receive_new_messages(user_id=user_id, session=session)
    if isinstance(messages, str):
        return jsonify({"error": messages}), 400
    
    return jsonify({"messages": messages}), 200

@app.route('/load_chat/', methods=['POST'])
async def load_chat():
    try:
        data = await request.get_json()
        session, chat_id, count = data.get('session'), data.get('chat_id'), data.get('count', 20)
        chat_id = str(chat_id)
    
        if not session or not chat_id:
            return jsonify({"error": "Session and chat id are required!"}), 400
        if not chat_id.isdigit():
            return jsonify({"error": "Invalid chat_id"}), 400
        chat_id = int(chat_id)

        user_id = int(session.split('@')[0])
        user_details = await user.get_user_details(user_id)
    
        if not user_details or user_details.get('session') != session:
            return jsonify({"error": "Invalid session"}), 400

        chat_data = await message.load_chat(chat_id=chat_id, user_id=user_id, session=session, count=count)
        if isinstance(chat_data, str):
            return jsonify({"error": chat_data}), 400
    
        return jsonify({"chat_data": chat_data}), 200
    except Exception as e:
        return jsonify({"error": e}), 400
