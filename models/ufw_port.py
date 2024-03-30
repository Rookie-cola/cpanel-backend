import time

from FlaskAppSingleton import FlaskAppSingleton

db = FlaskAppSingleton().get_db()


class ufw_port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.String(512), nullable=False)
    protocol = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), nullable=False)

    def __init__(self, port, protocol, description):
        self.port = port
        self.protocol = protocol
        self.description = description
