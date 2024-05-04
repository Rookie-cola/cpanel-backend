import os
from flask import request, jsonify, Blueprint
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
import docker
import time
from dateutil.parser import isoparse

app = FlaskAppSingleton().get_app()

docker_manager = Blueprint('docker', __name__)


# 获取镜像列表
@docker_manager.route('/images_list', endpoint="handle_docker_images_list", methods=['GET'])
@auth.login_required
def handle_docker_images_list():
    if request.method == 'GET':
        images = os.popen('docker images').read()
        # 解析返回的结果，获取镜像列表, repository, tag, id, created, size
        image_list = []
        lines = images.split('\n')[1:]
        for line in lines:
            if line:
                image_info = line.split()
                repository = image_info[0]
                tag = image_info[1]
                image_id = image_info[2]
                created = ' '.join(image_info[3:6])
                size = image_info[-1]
                image_dict = {
                    'repository': repository,
                    'tag': tag,
                    'image_id': image_id,
                    'created': created,
                    'size': size
                }
                image_list.append(image_dict)
        return jsonify({'images': image_list, 'message': 'Get images list successfully.', 'code': 200})
    else:
        return jsonify({'message': 'Invalid request method.', 'code': 405})


# 拉取镜像
@docker_manager.route('/pull_images', endpoint="handle_docker_pull_images", methods=['POST'])
@auth.login_required
def handle_docker_pull_images():
    if request.method == 'POST':
        if 'image' in request.json:
            image = request.json['image']
            os.system(f'docker pull {image}')
            return jsonify({'message': 'Images pulled successfully.', 'code': 200})
        else:
            return jsonify({'message': 'Invalid request data.', 'code': 400})


# 移除镜像
@docker_manager.route('/remove_images', endpoint="handle_docker_remove_images", methods=['POST'])
@auth.login_required
def handle_docker_remove_images():
    # 接收参数：镜像ID
    if request.method == 'POST':
        image_id = request.args.get('image_id')
        if not image_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        os.system(f'docker rmi {image_id}')
        return jsonify({'message': 'Images removed successfully.', 'code': 200})
    else:
        return jsonify({'message': 'Invalid request method.', 'code': 405})


# 创建容器，接收参数：容器名称、镜像名称、容器与宿主机端口映射
@docker_manager.route('/create_container', endpoint="handle_docker_create_container", methods=['POST'])
@auth.login_required
def handle_docker_create_container():
    if request.method == 'POST':
        if 'container_name' in request.json and 'image_name' in request.json and 'port_mapping' in request.json:
            container_name = request.json['container_name']
            image_name = request.json['image_name']
            port_mapping = request.json['port_mapping'] # 宿主机端口:容器端口 如：8080:80
            # 创建容器
            os.system(f'docker run -d  -p {port_mapping} --name {container_name} {image_name}')
            return jsonify({'message': 'Container created successfully.', 'code': 200})
        else:
            return jsonify({'message': 'Invalid request data.', 'code': 400})


# 启动容器
@docker_manager.route('/start_containers', endpoint="handle_docker_start_containers", methods=['POST'])
@auth.login_required
def handle_docker_start_containers():
    if request.method == 'POST':
        container_id = request.args.get('container_id')
        if not container_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        os.system(f'docker start {container_id}')
        # 如果启动失败，捕获异常并返回错误信息
        try:
            client = docker.from_env()
            container = client.containers.get(container_id)
            if container.status == 'running':
                return jsonify({'message': 'Container started successfully.', 'code': 200})
            else:
                return jsonify({'message': 'Container start failed.', 'code': 500})
        except Exception as e:
            return jsonify({'message': f'Container start failed. {str(e)}', 'code': 500})
    else:
        return jsonify({'message': 'Invalid request data.', 'code': 400})


# 列出所有容器
@docker_manager.route('containers_list', endpoint="handle_docker_running_containers", methods=['GET'])
@auth.login_required
def handle_docker_containers_list():
    if request.method == 'GET':
        client = docker.from_env()
        container_list = []
        for container in client.containers.list(all=True):
            if container.attrs['State']['Status'] != 'exited':
                container_port = list(container.attrs['NetworkSettings']['Ports'].keys())[0]
                container_ip = container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
                host_ports_data = container.attrs['NetworkSettings']['Ports'][container_port][0]
                host_ip = host_ports_data["HostIp"]
                host_port = host_ports_data["HostPort"]
                host_ports = f"{host_ip}:{host_port}"
            else:
                container_ip = None
                host_ports = None
                container_port = None
                host_ip = None
                host_port = None
                host_ports = None
                host_ports_data = None
            image_name = container.attrs['Config']['Image']
            container_name = container.attrs['Name'].split('/')[1]
            container_id = container.id[:12]
            status = container.attrs['State']['Status']
            running_time = time.time() - int(isoparse(container.attrs['State']['StartedAt']).timestamp())
            running_time_str = time.strftime('%H:%M:%S', time.gmtime(running_time))
            running_time = running_time_str

            container_dict = {
                'container_id': container_id,
                'image_name': image_name,
                'container_name': container_name,
                'container_ip': container_ip,
                'container_port': container_port,
                'host_port': host_ports,
                'status': status,
                'running_time': running_time
            }
            container_list.append(container_dict)
        if not container_list:
            return jsonify({'message': 'No running containers.', 'code': 200})
        return jsonify(
            {'containers': container_list, 'message': 'Get running containers list successfully.', 'code': 200})
    else:
        return jsonify({'message': 'Invalid request method.', 'code': 405})


# 停止运行的容器
@docker_manager.route('/stop_containers', endpoint="handle_docker_stop_containers", methods=['POST'])
@auth.login_required
def handle_docker_stop_containers():
    if request.method == 'POST':
        container_id = request.args.get('container_id')
        if not container_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        os.system(f'docker stop {container_id}')
        return jsonify({'message': 'Container stopped successfully.', 'code': 200})
    else:
        return jsonify({'message': 'Invalid request method.', 'code': 405})


# 移除停止的容器
@docker_manager.route('/remove_stop_containers', endpoint="handle_docker_remove_containers", methods=['POST'])
@auth.login_required
def handle_docker_remove_containers():
    if request.method == 'POST':
        container_id = request.args.get('container_id')
        if not container_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        os.system(f'docker rm {container_id}')
    return jsonify({'message': 'Containers removed successfully.', 'code': 200})


# 重启容器
@docker_manager.route('/restart_containers', endpoint="handle_docker_restart_containers", methods=['POST'])
@auth.login_required
def handle_docker_restart_containers():
    if request.method == 'POST':
        container_id = request.args.get('container_id')
        if not container_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        os.system(f'docker restart {container_id}')
        return jsonify({'message': 'Container restarted successfully.', 'code': 200})
    return jsonify({'message': 'Invalid request method.', 'code': 405})


# 查询容器日志
@docker_manager.route('/container_logs', endpoint="handle_docker_container_logs", methods=['POST'])
@auth.login_required
def handle_docker_container_logs():
    if request.method == 'POST':
        container_id = request.args.get('container_id')
        if not container_id:
            return jsonify({'message': 'Invalid request data.', 'code': 400})
        logs = os.popen(f'docker logs {container_id}').read().split('\n')
        return jsonify({'logs': logs, 'code': 200})
    else:
        return jsonify({'message': 'Invalid request method.', 'code': 405})
