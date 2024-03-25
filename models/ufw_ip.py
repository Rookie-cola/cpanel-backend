import time

from FlaskAppSingleton import FlaskAppSingleton

db = FlaskAppSingleton().get_db()


class ufw_ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(512), nullable=False)
    protocol = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), nullable=False)

    def __init__(self, ip, protocol, description):
        self.ip = ip
        self.protocol = protocol
        self.description = description

