from FlaskAppSingleton import FlaskAppSingleton

db = FlaskAppSingleton().get_db()


class ufw_port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.String(512), nullable=False)
    protocol = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    is_allowed = db.Column(db.Boolean, default=True)

    def __init__(self, port, protocol, description, is_allowed):
        self.port = port
        self.protocol = protocol
        self.description = description
        self.is_allowed = is_allowed


