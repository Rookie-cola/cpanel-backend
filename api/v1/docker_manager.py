import os
from flask import request, jsonify, Blueprint
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton

app = FlaskAppSingleton().get_app()

docker = Blueprint('docker', __name__)


@docker.route('/version', endpoint="handle_docker_version", methods=['GET'])
@auth.login_required
def handle_docker_version():
    if request.method == 'GET':
        version = os.popen('docker --version').read()
        return jsonify({'version': version.strip()})
    else:
        return jsonify({'message': 'Invalid request method.'}), 405


@docker.route('/remove_images', endpoint="handle_docker_remove_images", methods=['POST'])
@auth.login_required
def handle_docker_remove_images():
    if request.method == 'POST':
        data = request.get_json()
        if 'images' in data:
            images = data['images']
            os.system(f'docker rmi {" ".join(images)}')
            return jsonify({'message': 'Images removed successfully.'})
        else:
            return jsonify({'message': 'Invalid request data.'}), 400


@docker.route('/pull_images', endpoint="handle_docker_pull_images", methods=['POST'])
@auth.login_required
def handle_docker_pull_images():
    if request.method == 'POST':
        data = request.get_json()
        if 'images' in data:
            images = data['images']
            for image in images:
                os.system(f'docker pull {image}')
            return jsonify({'message': 'Images pulled successfully.'})
        else:
            return jsonify({'message': 'Invalid request data.'}), 400


@docker.route('/images_list', endpoint="handle_docker_images_list", methods=['GET'])
@auth.login_required
def handle_docker_images_list():
    if request.method == 'GET':
        images = os.popen('docker images').read()
        # 解析返回的结果，获取镜像列表, repository, tag, id, created, size
        image_list = []
        for image in images.split('\n')[1:]:
            if image:
                image_info = image.split('   ')
                image_list.append({
                   'repository': image_info[0],
                    'tag': image_info[1],
                    'id': image_info[2],
                    'created': image_info[3],
                   'size': image_info[4]
                })

        return jsonify({'images': image_list})
    else:
        return jsonify({'message': 'Invalid request method.'}), 405


