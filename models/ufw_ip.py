from FlaskAppSingleton import FlaskAppSingleton

db = FlaskAppSingleton().get_db()


class UfwIp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(512), nullable=False)
    protocol = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    is_allowed = db.Column(db.Boolean, nullable=False)

    def __init__(self, ip, protocol, description, is_allowed=True):
        self.ip = ip
        self.protocol = protocol
        self.description = description
        self.is_allowed = is_allowed


