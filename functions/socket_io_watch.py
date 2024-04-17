from system_watch import SystemWatch


def socket_io_systemwatch(socketio):
    while True:
        socketio.sleep(1)
        socketio.emit(
            'sys_info', {
                'cpu_info': SystemWatch.get_cpu_info(),
                'mem_info': SystemWatch.get_mem_info(),
                'disk_info': SystemWatch.get_disk_info(),
                'io_info': SystemWatch.get_io_info()
            }
        )
