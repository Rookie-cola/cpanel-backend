import psutil
from subprocess import getoutput


class ProcessManager:
    def __init__(self, pid):
        self.pid = pid
        pass

    @staticmethod
    def get_processes():
        process = []
        for i in psutil.pids():
            proc = psutil.Process(i)
            if proc.exe() not in process:
                process.append({
                    "pid": i,
                    "proc_name": proc.name(),
                    "cpu": round(proc.cpu_percent(), 2),
                    "mem": round(proc.memory_percent(), 2),
                    "status": proc.status()
                })
        return process

    def kill_process(self):
        print("kill -9 " + self.pid)
        return getoutput("kill -9 " + self.pid)

    def get_process(self):
        proc = psutil.Process(self.pid)
        return {
            "proc_name": proc.name(),
            "cpu": round(proc.cpu_percent(), 2),
            "mem": round(proc.memory_percent(), 2),
            "status": proc.status(),
            # "cmdline": " ".join(proc.cmdline())
        }
