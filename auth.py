from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request, jsonify
from decorators import auth
from dictionary.http_dict import login_dict
from FlaskAppSingleton import FlaskAppSingleton
from models import Users, Tokens
import time

app = FlaskAppSingleton().get_app()
db = FlaskAppSingleton().get_db()


def generate_token(user_id, user_name):
    # generate a token here
    expires_at = int(time.time()) + 60 * 60 * 24 * 30  # 30 days
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 24 * 30)
    token = None
    try:
        token = s.dumps({"id": user_id, "name": user_name}).decode("ascii")
        token_obj = Tokens(user_id, token, expires_at)
        db.session.add(token_obj)
        db.session.commit()

        app.logger.info("获取token成功:{}".format(token))
    except Exception as e:
        app.logger.error("获取token失败:{}".format(e))
    return token


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Missing username or password"}), 400

    user = Users.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({"code": login_dict.success.status_code, "message": login_dict.success.message,
                        "data": {"user": user.username, "token": generate_token(user.id, user.username)}}), 200
    else:
        return jsonify(
            {"code": login_dict.invalid.status_code, "message": login_dict.invalid.message, "data": None}), 401


@app.route('/logout', methods=['GET'])
@auth.login_required
def logout():
    Tokens.query.filter_by(token=request.headers.get('Authorization').replace('Bearer ', '')).delete()
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200
