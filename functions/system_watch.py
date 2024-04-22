from subprocess import getoutput
import psutil
from time import sleep
from models import ProcessManager


class SystemWatch:  # 系统监控类
    def __init__(self):
        pass

    @staticmethod
    def get_cpu_info():  # 获取CPU信息
        cpu = {
            'model_name': getoutput('cat /proc/cpuinfo | grep "model name" | uniq').split(':')[1][1:],
            'cpu_num': int(getoutput('cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l')),
            'core_num': int(getoutput('cat /proc/cpuinfo | grep "cpu cores" | wc -l')),
            'processor_num': int(getoutput('cat /proc/cpuinfo | grep "processor" | wc -l'))
        }
        return cpu

    @staticmethod
    def get_cpu_percent():  # 获取CPU使用率
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_mem_info():  # 获取内存信息
        with open('/proc/meminfo') as f:
            mem = {}
            cnt = 0
            for line in f:
                tmp = line.split(' ')
                # GB 表示
                mem[tmp[0][:-1]] = round(int(tmp[len(tmp) - 2]) / 2 ** 20, 2)

                cnt += 1
                if cnt > 6:
                    break

            mem['Used'] = round(mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached'], 2)
        return mem

    @staticmethod
    def get_disk_info():  # 获取磁盘信息
        return {
            'Used': round(psutil.disk_usage('/').used / 2 ** 30),
            'Total': round(psutil.disk_usage('/').total / 2 ** 30)
        }

    @staticmethod
    def get_io_info():  # 获取网络和磁盘IO信息
        pre_net_io_sent = psutil.net_io_counters().bytes_sent
        pre_net_io_recv = psutil.net_io_counters().bytes_recv
        pre_io_sent = psutil.disk_io_counters().write_bytes
        pre_io_recv = psutil.disk_io_counters().read_bytes
        sleep(1)
        cur_net_io_sent = psutil.net_io_counters().bytes_sent
        cur_net_io_recv = psutil.net_io_counters().bytes_recv
        cur_io_sent = psutil.disk_io_counters().write_bytes
        cur_io_recv = psutil.disk_io_counters().read_bytes
        return {
            'net_io_sent': round((cur_net_io_sent - pre_net_io_sent)),
            'net_io_recv': round((cur_net_io_recv - pre_net_io_recv)),
            'io_sent': round((cur_io_sent - pre_io_sent)),
            'io_recv': round((cur_io_recv - pre_io_recv))
        }

    @staticmethod
    def get_netstat_info():  # 获取所有tcp连接
        result = []
        for i in psutil.net_connections():
            if i.status == 'ESTABLISHED':
                result.append(ProcessManager(i.pid).get_process())
                # result[-1]["laddr_ip"] = i.laddr.ip
                # result[-1]["laddr_port"] = i.laddr.port
                # result[-1]["raddr_ip"] = i.raddr.ip
                # result[-1]["raddr_port"] = i.raddr.port
        return result
