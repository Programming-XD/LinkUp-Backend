import os
from flask import Flask
from app import app
from app.functions.login import login_bp

# REGISTER

app.register_blueprint(login_bp)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port) 
