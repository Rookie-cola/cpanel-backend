from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FlaskAppSingleton import FlaskAppSingleton
from models import Tokens
import time

app = FlaskAppSingleton().get_app()
db = FlaskAppSingleton().get_db()


def generate_token(user_id, user_name):
    expires_at = int(time.time()) + 60 * 60 * 24 * 7  # 过期时间为7天
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

