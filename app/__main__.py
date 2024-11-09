from flask import Flask
from app import app

@app.route('/', methods=['POST'])
async def ntg():
    return 'hi'

if __name__ == '__main__':
    app.run(debug=True)
