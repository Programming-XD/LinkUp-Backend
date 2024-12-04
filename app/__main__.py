import os
from app import app
from app.functions.login import login_bp
from app.functions.message import message_bp
from app.functions.eval import eval_bp
from app.functions.logs import logs_bp
from app.functions.chatlist import chatlist_bp
from app.functions.signup import signup_bp
from app.functions.check_session import check_session_bp
from quart_cors import cors
import asyncio
from quart import request, jsonify, Blueprint

cors(app)

# REGISTER
app.register_blueprint(login_bp)
app.register_blueprint(message_bp)
app.register_blueprint(eval_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(chatlist_bp)
app.register_blueprint(check_session_bp)
app.register_blueprint(signup_bp)



@app.route('/')
def home():
    return jsonify({'success': 'server online'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    
