from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
from .. import app, clients
import asyncio
import logging
from ..utilities import WebsocketHelper


# eg of clients[user_id]
"""
{
  "websockets": [],
  
}
"""
@app.websocket("/ws/")
async def ilymano(ws: WebSocket):
  global clients
  await ws.accept()
  while ws.client_state != WebSocketState.DISCONNECTED:
    try:
      txt = await ws.receive_text()
      asyncio.create_task(WebsocketHelper(txt, ws))
    except Exception as e:
      logging.info(e)
      break