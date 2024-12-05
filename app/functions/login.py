from app import app
from app.database.user import User
from quart import request, jsonify, Blueprint

user = User()

login_bp = Blueprint('login', __name__)


@app.route('/login/', methods=['POST'])
async def login():
    data = await request.get_json()
    username = str(data.get('username')).lower()
    password = data.get('password')
    session = data.get('session') or None

    user_ipp = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_ip = user_ipp.split(',')[0].strip() if user_ipp else None
    
    if session and len(session) >= 11:
        if '@' not in session:
            return jsonify({"error": "INVALID SESSION FORMAT"}), 400
        user_id = session.split('@')[0]
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            return jsonify({"error": "Invalid session"}), 400
        result = await user.login(session=session, username=user_id)
    else:
        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400
        result = await user.login(username=username, password=password, ip=user_ip)

    if result.startswith('success'):
        return jsonify({"message": result}), 200
    elif result.startswith('INVALID USER'):
        return jsonify({"error": 'INVALID USER'}), 400
    else:
        return (
            jsonify({"error": result}), 400,
            {"Access-Control-Allow-Origin": "*", "Custom-Header": "value"}
        )
