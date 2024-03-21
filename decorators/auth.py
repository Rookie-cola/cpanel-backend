import functools

from flask import request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from models import Tokens


def login_required(view_func):
    functools.wraps(view_func)

    def verify_token(*arg, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["Authorization"].replace("Bearer ", "")
        except Exception as e:
            # 没接收的到token,给前端抛出错误
            return jsonify(code=101, msg='缺少参数token')
        s = Serializer("test")
        try:
            user = s.loads(token)
        except Exception as e:
            print(e)
            return jsonify(code=403, msg="登录已过期")
        try:
            if Tokens.query.filter_by(token=token).first() is None:
                return jsonify(code=403, msg="Invalid token")
        except Exception as e:
            return jsonify(code=500, msg="Internal Server Error")
        return view_func(*arg, **kwargs)

    return verify_token
