import copy
import gc
from threading import Thread
from time import sleep
import _thread
import psutil
from flask import request, jsonify, Blueprint
from decorators import auth
from models.process import ProcessManager
from FlaskAppSingleton import FlaskAppSingleton
from functions import SystemWatch

app = FlaskAppSingleton().get_app()
pm = Blueprint('pm', __name__)

PROCESS_LIST = []


def get_process_list():
    global PROCESS_LIST
    while True:
        gc.collect()
        for proc in psutil.process_iter():
            if proc.name().strip() == '':
                continue
            average_cpu_usage = []
            for i in range(2):
                p = psutil.Process(proc.pid)
                p_cpu = p.cpu_percent(interval=0.1)
                average_cpu_usage.append(p_cpu)
            cpu_usage = round(float(sum(average_cpu_usage)) / len(average_cpu_usage), 2)
            if proc.pid in [p['pid'] for p in PROCESS_LIST]:
                for p in PROCESS_LIST:
                    if p['pid'] == proc.pid:
                        p['used_memory'] = round(proc.memory_percent() * 1024, 2)
                        p['cpu_percent'] = cpu_usage
                        p['status'] = proc.status()
                        break
            else:
                PROCESS_LIST.append({
                    'pid': proc.pid,
                    'username': proc.username(),
                    'proc_name': proc.name(),
                    'used_memory': round(proc.memory_percent() * 1024, 2),
                    'cpu_percent': cpu_usage,
                    "status": proc.status()
                })
        sleep(1)


# start a new thread to get process information
_thread.start_new_thread(get_process_list, ())


@pm.route('/process_manage', endpoint='process_manager_api', methods=['GET', 'DELETE'])
@auth.login_required
def process_api():
    if request.method == 'GET':
        try:
            return jsonify(PROCESS_LIST), 200
        except Exception as e:
            return jsonify({'error': 'Failed to get processes', 'details': str(e)}), 500

    elif request.method == 'DELETE':
        pid = request.args.get('pid')
        if not pid:
            return jsonify({'error': 'Missing pid parameter'}), 400
        try:
            result = ProcessManager(pid).kill_process()
            if 'Operation not permitted' in result:
                return jsonify({'error': 'Operation not permitted'}), 403
            if 'No such process' in result:
                return jsonify({'error': 'Process not found'}), 404
            return jsonify({'status': 'Process terminated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
