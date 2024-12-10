import os
from app import app
from quart_cors import cors
import asyncio
from quart import request, jsonify, Blueprint

app = cors(app, allow_origin="*")

# BLUEPRINT REGISTER
from app.functions.login import login_bp
from app.functions.message import message_bp
from app.functions.eval import eval_bp
from app.functions.logs import logs_bp
from app.functions.chatlist import chatlist_bp
from app.functions.signup import signup_bp
from app.functions.check_session import check_session_bp
from app.functions.user_info import userinfo_bp as user_info_bp

app.register_blueprint(login_bp)
app.register_blueprint(message_bp)
app.register_blueprint(eval_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(chatlist_bp)
app.register_blueprint(check_session_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(user_info_bp)

# WS BLUEPRINTS -------------

from app.ws.loadMsg import loadMsg_bp
from app.ws.chatlist import chatlist_bp as chatlistws_bp
from app.ws.sendMessage import sendMessage_bp

app.register_blueprint(loadMsg_bp)
app.register_blueprint(chatlistws_bp)
app.register_blueprint(sendMessage_bp)

# --------------------------------------------------#
    
@app.route('/')
def home():
    return jsonify({'success': 'server online'})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

# Hello world #
