from flask import request, jsonify, Blueprint

from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from functions.ufw_manager import PortManager, IPManager

app = FlaskAppSingleton().get_app()

ufw = Blueprint('ufw', __name__)


@ufw.route('/port', endpoint="handle_ufw_port", methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def handle_ufw_port():
    if request.method == 'GET':
        return jsonify(PortManager.get_allow_port())
    elif request.method == 'DELETE':
        PortManager(request.form['port'], request.form['protocol']).delete_allow_port()
        return jsonify({"status": "OK"})
    elif request.method == 'POST':
        status, msg = PortManager(request.form['port'], request.form['protocol']).add_allow_port(request.form['description'])
        return jsonify({"status": status, "msg": msg})


@ufw.route('/ip', endpoint="handle_ufw_ip", methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def handle_ufw_ip():
    if request.method == 'GET':
        return jsonify(IPManager.get_deny_ip())
    elif request.method == 'DELETE':
        IPManager(request.form['ip'], request.form['protocol']).delete_deny_ip()
        return jsonify({"status": "OK"})
    elif request.method == 'POST':
        status, msg = IPManager(request.form['ip'], request.form['protocol']).add_deny_ip(request.form['description'])
        return jsonify({"status": status, "msg": msg})
