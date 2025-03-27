import os
from .. import app
from quart_cors import cors
import asyncio
from quart import request, jsonify, Blueprint

app = cors(app, allow_origin="*")

# WS BLUEPRINTS -------------
from .ws.main import MainBp

app.register_blueprint(MainBp)
# --------------------------------------------------#
    
@app.route('/')
def home():
  return jsonify({'message': 'server online'}), 200

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(debug=True, host="0.0.0.0", port=port)