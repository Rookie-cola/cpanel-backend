import time

from FlaskAppSingleton import FlaskAppSingleton
db = FlaskAppSingleton().get_db()
class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(512), nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, token, expires_at):
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at

    def is_valid(self):
        return time.time() < self.expires_at