import io
import sys
import traceback
import asyncio
from datetime import datetime
import os
from subprocess import getoutput as run
from app import app
from app.database.message import *
from app.database.user import *
from quart import request, jsonify, Blueprint

eval_bp = Blueprint('eval', __name__)

def p(text):
    print(text)

@app.route('/api/dev/eval/', methods=['POST'])
async def eval():
    data = await request.get_json()
    if data.get('password') != 'manoiloveyou0/1':
        logging.warning('Someone trying to get access if password matches 50% password will changed')
        return jsonify({"error": "YOU ARE IMPOSTER"}), 400
    cmd = data.get('code')
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "INPUT: "
    final_output += f"{cmd}\n\n"
    final_output += "OUTPUT:\n"
    final_output += f"{evaluation.strip()} \n"
    output_code = evaluation.strip()
    
    return jsonify({"output": output_code})

async def aexec(code):
    local_vars = {}
    global_vars = globals()
    exec(
        "async def __aexec(): " + "".join(f"\n {line}" for line in code.split("\n")),
        global_vars,
        local_vars
    )
    return await local_vars["__aexec"]()
