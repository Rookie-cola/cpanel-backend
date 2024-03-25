from flask_login import UserMixin

from FlaskAppSingleton import FlaskAppSingleton

db = FlaskAppSingleton().get_db()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
