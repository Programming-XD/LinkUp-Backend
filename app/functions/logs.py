from app import app
from app.database.message import *
from app.database.user import *
from quart import request, jsonify, Blueprint
from subprocess import getoutput as run

logs_bp = Blueprint('logs', __name__)

@app.route('/api/dev/logs/', methods=['POST'])
async def logs():
    data = await request.get_json()
    if not data.get('password'):
        return jsonify({"error": "No access"}), 400
    if data.get('password') != 'manoiloveyou0/1':
        logging.warning('Unauthorized access attempt detected.')
        return jsonify({"error": "YOU ARE IMPOSTER"}), 400
    output = run('tail log.txt')
    return jsonify({"output": output})
