# import flask
# from flask import request, jsonify, abort, Blueprint
# from models.nginx import NginxManager
# from decorators import auth
# from FlaskAppSingleton import FlaskAppSingleton
#
# app = FlaskAppSingleton().get_app()
#
# web = Blueprint('website_manager', __name__)
#
#
# @web.route('/website', methods=['GET', 'DELETE', 'PATCH'])
# @auth.login_required
# def website_manager():
#     if request.method == 'GET':
#         return get_web_list()
#     elif request.method == 'DELETE':
#         return delete_nginx_site()
#     elif request.method == 'PATCH':
#         return update_nginx_site()
#     else:
#         abort(405)
#
#
# def get_web_list() -> flask.Response:
#     web_list = NginxManager.get_web_list()
#     result = [{"name": i[0], "port": i[1]} for i in web_list]
#     return jsonify({"result": result})
#
#
# def delete_nginx_site():
#     name = request.form.get('name')
#     if not name:
#         return jsonify({"error": "Missing 'name' parameter"}), 400
#
#     try:
#         NginxManager(name).delete_file()
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#     return jsonify({"status": "OK"})
#
#
# def update_nginx_site():
#     file = request.files.get('file')
#     if not file:
#         return jsonify({"error": "Missing 'file'"}), 400
#
#     port = request.form.get('port')
#     if not port or not port.isdigit():
#         return jsonify({"error": "Invalid 'port'"}), 400
#
#     try:
#         NginxManager(file.filename.split('.')[0]).upload(file, int(port))
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#     return jsonify({"status": "OK"})
