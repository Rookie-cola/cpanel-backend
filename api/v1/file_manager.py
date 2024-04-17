import os
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
        path = request.args.get('path', '/')  # 若未提供路径，默认为根目录 '/'
        file_manager = FileManager(path)
        file_list = file_manager.get_file_list()
        return jsonify({"file": file_list})
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

    elif request.method == 'DELETE':
        # 删除文件
        response = file_manager.delete_file(request.args.get('filename'))
        return jsonify(response)

    elif request.method == 'POST':
        # 上传文件
        uploaded_file = request.files.get('file')
        if uploaded_file:
            response = file_manager.upload(uploaded_file)
            return jsonify(response)
        else:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
