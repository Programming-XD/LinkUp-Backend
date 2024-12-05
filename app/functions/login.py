from app import app
from app.database.user import User
from quart import request, jsonify, Blueprint
from quart_cors import cors_origin

user = User()

login_bp = Blueprint('login', __name__)


@app.route('/login/', methods=['POST'])
@cors_origin(allow_origin="*")
async def login():
    data = await request.get_json()
    username = str(data.get('username')).lower()
    password = data.get('password')
    session = data.get('session')

    
    if session:
        if '@' not in session:
            return jsonify({"error": "INVALID SESSION FORMAT"}), 400
        user_id = int(session.split('@')[0])
        result = await user.login(session=session, username=user_id)
    else:
        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400
        result = await user.login(username=username, password=password)

    if result.startswith('success'):
        return jsonify({"message": result}), 200
    elif result.startswith('INVALID USER'):
        return jsonify({"error": 'INVALID USER'}), 400
    else:
        return (
            jsonify({"error": result}), 400,
            {"Access-Control-Allow-Origin": "*", "Custom-Header": "value"}
        )
