from app import app
from app.database.message import *
from app.database.user import *
from quart import request, jsonify, Blueprint

user=User()
message=Message()

@app.route('/send_message/', methods=['POST'])
async def send():
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

