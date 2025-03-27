from quart import Blueprint, websocket
import json

MainBp, ws, clients = Blueprint("ws", __name__), websocket, {}

@MainBp.on_websocket("/ws/")
async def otazuki():
  global clients
  while True:
    data = await websocket.receive_bytes()
    message = data.decode("utf-8")
    try:
      data = json.loads(message)
      """ 
      - After LoggedIn
      clients[websocket] = {"auth_key": key, "session_id": 123}
      """
    except json.JSONDecodeError:
      await websocket.send(json.dumps({"code": 400, "message": "Cannot decode input into json. invalid input."}))