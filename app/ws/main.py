from quart import Blueprint, websocket
import json

MainBp = Blueprint("ws", __name__)
clients = {}

