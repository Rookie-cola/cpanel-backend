from FlaskAppSingleton import FlaskAppSingleton
from flask import jsonify, Blueprint
from decorators import auth
from functions import SystemWatch

# 获取flask app实例
app = FlaskAppSingleton().get_app()
system = Blueprint('system', __name__)


@system.route('/info', endpoint='get_system_info', methods=['GET'])
@auth.login_required
def get_system_info():
    return jsonify({
        'cpu_info': SystemWatch.get_cpu_info(),
        'cpu_percent': SystemWatch.get_cpu_percent(),
        'mem_info': SystemWatch.get_mem_info(),
        'disk_info': SystemWatch.get_disk_info(),
        'io_info': SystemWatch.get_io_info()
    })


@system.route('/netstat', endpoint='get_netstat', methods=['GET'])
@auth.login_required
def get_netstat():
    return jsonify(SystemWatch.get_netstat_info()[:20])
