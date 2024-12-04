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
    else:
        return jsonify({"error": result}), 400
