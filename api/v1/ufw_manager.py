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
    is_allowed_str = request.form.get('is_allowed')
    description = request.form.get('description')

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        # limit = request.args.get('limit', 1, type=int)
        limit = 999999
        ports = PortManager.get_port(page=page, limit=limit)
        if not ports:
            return jsonify({"status": False, "msg": "暂无端口数据"})
        return jsonify(ports)

    else:  # 处理非 GET 请求（POST、DELETE）
        if request.method == 'POST':
            if is_allowed_str is None or is_allowed_str == "":
                return jsonify({"status": False, "msg": "'is_allowed' 字段不能为空"})

            is_allowed = is_allowed_str.lower() in ['true', '1']
            port_manager = PortManager(port=port, protocol=protocol, description=description, is_allowed=is_allowed)
            status, msg = port_manager.add_port()
            return jsonify({"status": status, "msg": msg})
        elif request.method == 'DELETE':
            if request.args.get('rule_id') is None:
                return jsonify({"status": False, "msg": "rule_id 不能为空"})
            status, msg = PortManager.delete_port_by_id(request.args.get('rule_id'))
            return jsonify({"status": status, "msg": msg})


@ufw.route('/ip', endpoint="handle_ufw_ip", methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def handle_ufw_ip():
    ip = request.form.get('ip')
    protocol = request.form.get('protocol')
    is_allowed_str = request.form.get('is_allowed')
    description = request.form.get('description')

    if request.method == 'GET':
        ips = IPManager.get_ip()
        if not ips:
            return jsonify({"status": False, "msg": "暂无地址数据"})
        return jsonify(IPManager.get_ip())
    else:  # 处理非 GET 请求（POST、DELETE）
        if request.method == 'POST':
            if is_allowed_str is None or is_allowed_str == "":
                return jsonify({"status": False, "msg": "'is_allowed' 字段不能为空"})

            is_allowed = is_allowed_str.lower() in ['true', '1']
            ip_manager = IPManager(ip=ip, protocol=protocol, description=description, is_allowed=is_allowed)
            status, msg = ip_manager.add_ip()
            return jsonify({"status": status, "msg": msg})
        elif request.method == 'DELETE':
            if request.args.get('rule_id') is None:
                return jsonify({"status": False, "msg": "rule_id 不能为空"})
            status, msg = IPManager.delete_ip_by_id(request.args.get('rule_id'))
            return jsonify({"status": status, "msg": msg})
