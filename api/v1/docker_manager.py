import os

from flask import request, jsonify, Blueprint

from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton

app = FlaskAppSingleton().get_app()

docker = Blueprint('docker', __name__)


@docker.route('/version', endpoint="handle_docker_version", methods=['GET'])
@auth.login_required
def handle_docker_version():
    if request.method == 'GET':
        version = os.popen('docker --version').read()
        return jsonify({'version': version.strip()})
    else:
        return jsonify({'message': 'Invalid request method.'}), 405
