import json

async def create_response(data_id, reply, force_dump=True):
  data = {
    "updateType": "response",
    "reply": reply,
    "replyOf": data_id,
  }
  if force_dump:
    return json.dumps(data)
  return data