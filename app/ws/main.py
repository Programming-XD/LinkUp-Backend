from quart import Blueprint, websocket
import json

MainBp, ws = Blueprint("ws", __name__), websocket

@MainBp.on_websocket("/ws/")
async def otazuki():
  
  while True:
    data = await websocket.receive_bytes()
    message = data.decode("utf-8")
    try:
      data = json.loads(message)
    except json.JSONDecodeError:
      await websocket.send(json.dumps({"code": 400, "message": "Cannot decode input into json. invalid input."}))