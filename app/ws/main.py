from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from .. import app
import asyncio

@app.websocket("/ws/")
async def ilymano(ws: WebSocket):
  await ws.accept()
  while True:
    try:
      await ws.receive_text()
    except WebSocketDisconnect:
      print("Op")
  #await xyz(ws)