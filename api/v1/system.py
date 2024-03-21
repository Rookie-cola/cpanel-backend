from flask import jsonify, Blueprint

from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton

app = FlaskAppSingleton().get_app()

system = Blueprint('system', __name__)


@system.route('/info', endpoint='get_system_info', methods=['GET'])
@auth.login_required
def get_system_info():
    # psutil 获取系统信息
    import psutil
    import platform

    # 获取硬盘信息
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.mountpoint] = {
            'total': str(round(usage.total / (1024.0 ** 3))) + " GB",
            'used': str(round(usage.used / (1024.0 ** 3))) + " GB",
            'free': str(round(usage.free / (1024.0 ** 3))) + " GB",
            'percent': usage.percent,
            'fstype': partition.fstype
        }

    system_info = {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        'cpu_count': psutil.cpu_count(),
        'cpu_percent': psutil.cpu_percent(),
        'boot_time': str(psutil.boot_time()),
        'disk_info': disk_info
    }
    return jsonify(system_info)
