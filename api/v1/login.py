from flask import request, jsonify
from decorators import auth
from dictionary.http_dict import login_dict
from FlaskAppSingleton import FlaskAppSingleton
from models import Users, Tokens
from functions.auth import generate_token

app = FlaskAppSingleton().get_app()
db = FlaskAppSingleton().get_db()


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


@app.route('/logout', methods=['POST'])
@auth.login_required
def logout():
    Tokens.query.filter_by(token=request.headers.get('Authorization').replace('Bearer ', '')).delete()
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200
