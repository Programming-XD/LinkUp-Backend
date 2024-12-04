from app import app
from app.database.user import User
from quart import request, jsonify, Blueprint

user = User()

signup_bp = Blueprint('signup', __name__)

@app.route('/signup/', methods=['POST'])
async def sign_up():
    data = await request.get_json()
    name = data.get('name')
    username = str(data.get('username')).lower()
    password = data.get('password')

    if not name or not username or not password:
        return jsonify({"error": "All fields are required!"}), 400

    result = await user.sign_up(name, username, password)

    if result.startswith('success'):
        return jsonify({"message": result}), 200
    else:
        return jsonify({"error": result}), 400

