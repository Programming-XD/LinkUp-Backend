import logging
from quart import Quart
from quart_cors import cors

# LOGGING
logging.basicConfig(
  format="[LinkUp-Backend] %(name)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)
app = Quart(__name__)