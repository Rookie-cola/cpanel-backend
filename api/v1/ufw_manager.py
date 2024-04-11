from flask import request, jsonify, Blueprint
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from functions.ufw_manager import PortManager, IPManager


app = FlaskAppSingleton().get_app()
ufw = Blueprint('ufw', __name__)


@ufw.route('/port', endpoint="handle_ufw_port", methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def handle_ufw_port():
    port = request.form.get('port')
    protocol = request.form.get('protocol')
    is_allowed = request.form.get('is_allowed').lower() in ['true', '1']
    description = request.form.get('description')
    if request.method == 'GET':
        ports = PortManager.get_port()
        if not ports:
            return jsonify({"status": False, "msg": "暂无端口数据"})
        return jsonify(PortManager.get_port())
    elif request.method == 'POST':
        port_manager = PortManager(port=port, protocol=protocol,description=description, is_allowed=is_allowed)
        status, msg = port_manager.add_port()
        return jsonify({"status": status, "msg": msg})
    elif request.method == 'DELETE':
        port_manager = PortManager(port=port, protocol=protocol, description=description, is_allowed=is_allowed)
        status, msg = port_manager.delete_port()
        return jsonify({"status": status, "msg": msg})


@ufw.route('/ip', endpoint="handle_ufw_ip", methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def handle_ufw_ip():
    ip = request.form.get('ip')
    protocol = request.form.get('protocol')
    is_allowed = request.form.get('is_allowed').lower() in ['true', '1']
    description = request.form.get('description')
    if request.method == 'GET':
        ips = IPManager.get_ip()
        if not ips:
            return jsonify({"status": False, "msg": "暂无地址数据"})
        return jsonify(IPManager.get_ip())
    elif request.method == 'POST':
        ip_manager = IPManager(ip=ip, protocol=protocol, description=description, is_allowed=is_allowed)
        status, msg = ip_manager.add_ip()
        return jsonify({"status": status, "msg": msg})
    elif request.method == 'DELETE':
        ip_manager = IPManager(ip=ip, protocol=protocol, description=description, is_allowed=is_allowed)
        status, msg = ip_manager.delete_ip()
        return jsonify({"status": status, "msg": msg})
