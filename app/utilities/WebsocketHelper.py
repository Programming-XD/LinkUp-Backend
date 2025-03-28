import json
from app import *
import logging
from .create_response import create_response

async def check_data(data):
  # add decryption future..
  try: data = json.loads(data)
  except: return
  if data.get('method') and data.get('arguments') and data.get('data_id'):
    return data

async def WebsocketHelper(byt, ws):
  z = await check_data(byt)
  if z:
    method, args, data_id = z.get('method'), z.get('arguments'), z.get('data_id')
    if hasattr(server, method):
      try:
        await exec(f"server.{method}(**args)")
        await ws.send_text("fk")
      except TypeError as e:
        if "got an unexpected keyword argument" in str(e):
          r = await create_response(data_id, {'ok': False, 'message': "Unexpected argument"})
          return await ws.send_text(r)       
      except Exception as e:
        logging.info(e)
    # bruh use bytes