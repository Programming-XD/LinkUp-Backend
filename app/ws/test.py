from app import *
from quart import *

test_bp = Blueprint('test', __name__)

@test_bp.websocket('/ws/test/')
async def test():
  while True:
    msg = await websocket.receive()
    if msg:
      await websocket.send(msg)
    await websocket.send('Idk she love me or not')
