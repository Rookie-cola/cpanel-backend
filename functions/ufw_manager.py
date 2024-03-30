import os
from sqlalchemy.exc import IntegrityError
from FlaskAppSingleton import FlaskAppSingleton
from models.ufw_ip import ufw_ip
from models.ufw_port import ufw_port

db = FlaskAppSingleton().get_db()


class PortManager:
    def __init__(self, port=80, protocol='tcp'):
        self.port = port
        self.protocol = protocol

    def add_allow_port(self, description):
        ufw_port_obj = ufw_port(self.port, self.protocol, description)
        try:
            db.session.add(ufw_port_obj)
            db.session.commit()
        except IntegrityError:
            return False, "Port already exists"
        os.system("sudo ufw allow {}/{}".format(self.port, self.protocol))
        return True, "Port added successfully"

    @staticmethod
    def get_allow_port():
        ports = ufw_port.query.all()
        result = []
        for port in ports:
            result.append({
                "rule_id": port.id,
                "port": port.port,
                "protocol": port.protocol,
                "description": port.description
            })
        return result

    def delete_allow_port(self):
        db.session.query(ufw_port).filter_by(port=self.port, protocol=self.protocol).delete()
        db.session.commit()
        os.system("sudo ufw delete allow {}/{}".format(self.port, self.protocol))
        pass


class IPManager:
    def __init__(self, ip='127.0.0.1', protocol='tcp'):
        self.ip = ip
        self.protocol = protocol

    def add_deny_ip(self, description):
        ufw_ip_obj = ufw_ip(self.ip, self.protocol, description)
        try:
            db.session.add(ufw_ip_obj)
            db.session.commit()
        except IntegrityError:
            return False, "IP already exists"
        os.system("sudo ufw deny from {} proto {}".format(self.ip, self.protocol))
        return True, "IP added successfully"

    @staticmethod
    def get_deny_ip():
        ip_list = ufw_ip.query.all()
        result = []
        for ip in ip_list:
            result.append({
                "rule_id": ip.id,
                "ip": ip.ip,
                "protocol": ip.protocol,
                "description": ip.description
            })
        return result

    def delete_deny_ip(self):
        db.session.query(ufw_ip).filter_by(ip=self.ip, protocol=self.protocol).delete()
        db.session.commit()
        os.system("sudo ufw delete deny from {} proto {}".format(self.ip, self.protocol))


# if __name__ == '__main__':
#     # IPManager('192.168.1.1', 'tcp').add_deny_ip('test')
#     # print(IPManager.get_deny_ip())
#     IPManager('192.168.1.1', 'tcp').delete_deny_ip()
