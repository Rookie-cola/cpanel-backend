from api.v1.file_manager import file
from auth import logout, login
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from config import config
from api.v1 import system, ufw, docker, pm, file_manager

app = FlaskAppSingleton().get_app()
app.config['SECRET_KEY'] = config.SECRET_KEY


@app.route('/login', methods=['POST'])
def handle_login():
    return login()


@app.route('/logout', endpoint='logout', methods=['GET'])
@auth.login_required
def handle_logout():
    return logout()


app.register_blueprint(system, url_prefix='/api/v1/system')
app.register_blueprint(ufw, url_prefix='/api/v1/ufw')
app.register_blueprint(docker, url_prefix='/api/v1/docker')
app.register_blueprint(pm, url_prefix='/api/v1/process')
app.register_blueprint(file, url_prefix='/api/v1/file')

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
