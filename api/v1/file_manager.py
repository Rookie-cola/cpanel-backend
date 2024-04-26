import os
import zipfile

import flask
from flask import request, jsonify, Blueprint
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from models.file import FileManager

app = FlaskAppSingleton().get_app()
file = Blueprint('file', __name__)


@file.route('/file_list', endpoint='file_list', methods=['GET'])
@auth.login_required
def show_file_list():  # 显示文件列表
    try:
        path = request.args.get('path', '/')  # 默认路径为根目录
        file_manager = FileManager(path)
        file_list = file_manager.get_file_list()
        # 如果路径不存在，则返回404
        if not os.path.exists(path):
            return jsonify({"code": 404, "msg": "Path not found", "data": []})
        return jsonify({"code": 200, "msg": "success", "data": file_list})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@file.route('/file_handler', endpoint='file_handler', methods=['GET', 'DELETE', 'POST'])
@auth.login_required
def handle_file():
    path = request.values.get('path', '')  # 获取路径
    file_manager = FileManager(path)

    if request.method == 'GET':
        # 下载文件
        if os.path.isfile(path):
            return flask.send_file(path, as_attachment=True)
        else:
            return jsonify({"status": "error", "message": "File not found"}), 404

    if request.method == 'DELETE':
        # 删除文件
        response = file_manager.delete_file(request.args.get('path'))
        return jsonify(response)

    elif request.method == 'POST':
        # 上传文件
        uploaded_file = request.files.get('file')
        path = request.args.get('path', '')  # 获取路径
        if not os.path.exists(path):
            return jsonify({"status": "error", "message": "Path not found"}), 404
        if path == '/':
            return jsonify({"status": "error", "message": "Cannot upload to root directory"}), 403
        if path == '':
            return jsonify({"status": "error", "message": "Path not provided"}), 400
        if uploaded_file:
            response = file_manager.upload(uploaded_file, path)
            return jsonify(response)
        else:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400


# 解压文件
@file.route('/unzip_file', endpoint='unzip', methods=['POST'])
@auth.login_required
def handle_unzip():
    path = request.args.get('path')
    if path and os.path.isfile(path):
        f = zipfile.ZipFile(path, 'r')
        f.extractall(path.replace(path.split('/')[-1], '')[:-1])
        f.close()
        return jsonify({"status": "success", "message": "File unzipped successfully"})
    return jsonify({'status': 'error', 'message': 'error'})


