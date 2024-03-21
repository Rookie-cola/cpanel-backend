from flask_login import LoginManager

from auth import logout, login
from decorators import auth
from FlaskAppSingleton import FlaskAppSingleton
from models import Users

from api.v1.system import system


app = FlaskAppSingleton().get_app()
app.config['SECRET_KEY'] = 'test'

# 初始化登录管理器

username = 'admin'
password = 'admin'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'




# 路由注册
@app.route('/login', methods=['POST'])
def handle_login():
    return login()


@app.route('/logout', endpoint='logout', methods=['GET'])
@auth.login_required
def handle_logout():
    return logout()


app.register_blueprint(system, url_prefix='/api/v1/system')

if __name__ == '__main__':
    app.run(debug=True)
