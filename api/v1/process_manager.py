from flask import request, jsonify, Blueprint
from decorators import auth
from models.process import ProcessManager
from FlaskAppSingleton import FlaskAppSingleton
from functions import SystemWatch

app = FlaskAppSingleton().get_app()
pm = Blueprint('pm', __name__)


@pm.route('/process_manager', endpoint='process_manager_api', methods=['GET', 'DELETE'])
@auth.login_required
def process_api():
    if request.method == 'GET':
        try:
            return jsonify(SystemWatch.get_netstat_info()), 200
        except Exception as e:
            return jsonify({'error': 'Failed to get processes', 'details': str(e)}), 500
    elif request.method == 'DELETE':
        pid = request.form.get('pid')
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
