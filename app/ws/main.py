from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
from .. import app, clients, ws_datas
import asyncio
import logging
from ..utilities import WebsocketHelper


# eg of clients[user_id]
"""
{
  "websockets": [],
  
}
"""
# eg of ws_datas[ws]
"""
{
  "auth_key": None or key,
  "logged": bool: logged in a account,
  "device_session": None or session,
  "loggedAs": id of a account,
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
  if ws in ws_datas:
    del ws_datas[ws]