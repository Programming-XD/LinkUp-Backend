from app import app
from app.database.user import User
from flask import request, jsonify

user = User()

@app.route('/signup', methods=['POST'])
async def sign_up():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    if not name or not username or not password:
        return jsonify({"error": "All fields are required!"}), 400

    result = await user.sign_up(name, username, password)
    
    if result.startswith('success'):
        return jsonify({"message": result}), 200
    else:
        return jsonify({"error": result}), 400


@app.route('/login', methods=['POST'])
async def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    session = data.get('session')

    if session:
        result = await user.login(session=session)
    else:
        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400
        result = await user.login(username=username, password=password)

    if result.startswith('success'):
        return jsonify({"message": result}), 200
    else:
        return jsonify({"error": result}), 400
