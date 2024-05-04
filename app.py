from flask import jsonify
from flask_cors import CORS
from api.v1.login import login, logout
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from config import config
from api.v1 import system, ufw, docker_manager, pm, file, web

app = FlaskAppSingleton().get_app()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = config.SECRET_KEY

app.register_blueprint(system, url_prefix='/api/v1/system')
app.register_blueprint(ufw, url_prefix='/api/v1/ufw')
app.register_blueprint(docker_manager, url_prefix='/api/v1/docker')
app.register_blueprint(pm, url_prefix='/api/v1/process')
app.register_blueprint(file, url_prefix='/api/v1/file')
app.register_blueprint(web, url_prefix='/api/v1/website')


@app.route('/login', methods=['POST'])
def handle_login():
    return login()


@app.route('/user/info', endpoint='user_info', methods=['GET'])
def handle_user_info():
    return jsonify({"code": 200, "roles": ['admin'], "name": "name",
                    "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                    "introduction": "I am a super administrator"}), 200


@app.route('/logout', endpoint='logout', methods=['GET'])
@auth.login_required
def handle_logout():
    return logout()


if __name__ == '__main__':
    app.run(debug=True)
