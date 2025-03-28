import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from . import app

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get('/')
async def home():
  return {'message': 'server online'}

if __name__ == "__main__":
  first = False
  if not first:
    from .ws.main import *
    first = True
  import uvicorn
  port = int(os.environ.get("PORT", 8080))
  uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
  