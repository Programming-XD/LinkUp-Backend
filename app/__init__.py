import logging

# LOGGING
logging.basicConfig(
  format="[LinkUp-Backend] %(name)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.DEBUG,
)
from fastapi import FastAPI
app = FastAPI()
clients = {}
from .server import Server
server = Server()
ws_datas = {}