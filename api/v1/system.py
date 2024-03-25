from FlaskAppSingleton import FlaskAppSingleton
from flask import jsonify, Blueprint
from decorators import auth
import time, datetime
import psutil
import platform

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
    # 获取硬盘信息
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.fstype == 'ext4':
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.mountpoint] = {
                'total': str(round(usage.total / (1024.0 ** 3))) + " GB",
                'used': str(round(usage.used / (1024.0 ** 3))) + " GB",
                'free': str(round(usage.free / (1024.0 ** 3))) + " GB",
                'percent': usage.percent,
                'fstype': partition.fstype
            }
    # 获取系统信息
    system_info = {
        # 系统运行时间
        'sys_uptime': str(system_uptime),
        # CPU使用率
        'cpu_times': {
            'user': psutil.cpu_times().user,
            'system': psutil.cpu_times().system,
            'idle': psutil.cpu_times().idle,
            'nice': psutil.cpu_times().nice,
            'iowait': psutil.cpu_times().iowait,
            'irq': psutil.cpu_times().irq,
            'softirq': psutil.cpu_times().softirq,
            'steal': psutil.cpu_times().steal,
            'guest': psutil.cpu_times().guest,
            'guest_nice': psutil.cpu_times().guest_nice
        },
        # 内存使用率
        'virtual_memory': {
            'total': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
            'available': str(round(psutil.virtual_memory().available / (1024.0 ** 3))) + " GB",
            'percent': psutil.virtual_memory().percent,
            'used': str(round(psutil.virtual_memory().used / (1024.0 ** 3))) + " GB",
            'free': str(round(psutil.virtual_memory().free / (1024.0 ** 3))) + " GB"
        },
        # 主机名称
        'hostname': platform.node(),
        # 系统版本信息
        'platform': platform.system(),
        # 处理器架构信息
        'architecture': platform.machine(),
        # CPU数量
        'platform_release': platform.release(),
        # 内核版本信息
        'platform_version': platform.version(),
        'processor': platform.processor(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        # 系统启动时间
        'boot_time': str(time_str),
        # 硬盘信息
        'disk_info': disk_info
    }

    # 返回系统信息
    return jsonify(system_info)
