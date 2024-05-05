import psutil
from subprocess import getoutput


class ProcessManager:
    def __init__(self, pid):
        self.pid = pid
        pass

    def get_process(self):
        proc = psutil.Process(self.pid)
        average_cpu_usage = []
        for i in range(2):
            p = psutil.Process(self.pid)
            p_cpu = p.cpu_percent(interval=0.1)
            average_cpu_usage.append(p_cpu)
        cpu_usage = round(float(sum(average_cpu_usage)) / len(average_cpu_usage), 2)
        return {
            'pid': proc.pid,
            'username': proc.username(),
            'proc_name': proc.name(),
            'used_memory': round(proc.memory_percent() * 1024, 2),
            'cpu_percent': cpu_usage,
            "status": proc.status()
        }

    def kill_process(self):
        print("kill -9 " + self.pid)
        return getoutput("kill -9 " + self.pid)
