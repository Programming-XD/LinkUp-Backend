import logging
import io
import sys
import traceback
import asyncio
from datetime import datetime
import os
from subprocess import getoutput as run
from app import app
from app.database.message import *
from app.database.message import db as mdb 
from app.database.user import *
from app.database.user import db as udb
from quart import request, jsonify, Blueprint

eval_bp = Blueprint('eval', __name__)

@app.route('/api/dev/eval/', methods=['POST'])
async def eval():
    data = await request.get_json()
    if not data.get('password') or not data.get('code'):
        return jsonify({"error": "No access"}), 400
    if data.get('password') != 'manoiloveyou0/1':
        logging.warning('Unauthorized access attempt detected.')
        return jsonify({"error": "YOU ARE IMPOSTER"}), 400

    cmd = data.get('code')
    old_stderr, old_stdout = sys.stderr, sys.stdout
    redirected_output, redirected_error = io.StringIO(), io.StringIO()
    sys.stdout, sys.stderr = redirected_output, redirected_error
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr

    evaluation = exc if exc else stderr if stderr else stdout if stdout else "success"

    final_output = f"{evaluation.strip()}"
    
    return jsonify({"output": final_output})

async def aexec(code):
    local_vars = {}
    global_vars = globals()
    exec(
        "async def __aexec(): " + "".join(f"\n {line}" for line in code.split("\n")),
        global_vars,
        local_vars
    )
    return await local_vars["__aexec"]()
