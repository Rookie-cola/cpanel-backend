from FlaskAppSingleton import FlaskAppSingleton
from flask import jsonify, Blueprint
from decorators import auth
import time, datetime
import psutil
from functions import SystemWatch

# 获取flask app实例
app = FlaskAppSingleton().get_app()
system = Blueprint('system', __name__)

# 系统当前时间
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 系统启动时间
system_boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
# 系统运行时间
system_uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())


@system.route('/info', endpoint='get_system_info', methods=['GET'])
@auth.login_required
def get_system_info():
    return jsonify({
        'cpu_info': SystemWatch.get_cpu_info(),
        'mem_info': SystemWatch.get_mem_info(),
        'disk_info': SystemWatch.get_disk_info(),
        'io_info': SystemWatch.get_io_info()
    })


@system.route('/netstat', endpoint='get_netstat', methods=['GET'])
@auth.login_required
def get_netstat():
    return jsonify(SystemWatch.get_netstat_info()[:20])
