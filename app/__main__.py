import os
from . import *
from quart_cors import cors
import asyncio
from quart import request, jsonify, Blueprint

app = cors(app, allow_origin="*")

@app.route('/')
def home():
  return jsonify({'message': 'server online'}), 200

@app.websocket("/ws/")
async def otazuki():
  await websocket.send("hi")

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True, host="0.0.0.0", port=port)