import os
from flask import Flask
from app import app
from app.functions.login import login_bp
import asyncio

# REGISTER

app.register_blueprint(login_bp)

@app.route('/')
def home():
    return 'Hello, World!'

def run():
    port = int(os.environ.get("PORT", 5000))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run(debug=True, host="0.0.0.0", port=port))

if __name__ == "__main__":
    run()
    
