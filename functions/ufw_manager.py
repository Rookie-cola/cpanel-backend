import subprocess
from sqlalchemy.exc import IntegrityError
from FlaskAppSingleton import FlaskAppSingleton
from models.ufw_ip import UfwIp
from models.ufw_port import UfwPort

db = FlaskAppSingleton().get_db()
ufw_port = UfwPort
ufw_ip = UfwIp


class PortManager:
    def __init__(self, port, protocol, description, is_allowed):
        self.port = port
        self.protocol = protocol
        self.description = description
        self.is_allowed = is_allowed

    @staticmethod
    def get_port(page=1, limit=20):
        ports = ufw_port.query.paginate(page=page, per_page=limit, error_out=False)
        result = []
        for port in ports:
            result.append({
                "rule_id": port.id,
                "port": port.port,
                "protocol": port.protocol,
                "description": port.description,
                "is_allowed": port.is_allowed
            })
        return result

    def add_port(self):
        action = "allow" if self.is_allowed else "deny"
        if self.protocol.lower() not in ['tcp', 'udp']:
            return False, f"不支持的协议类型: {self.protocol}"

        command = f"sudo ufw {action} {self.port}/{self.protocol}"
        try:
            # 检查端口规则是否已存在
            existing_port = ufw_port.query.filter_by(port=self.port, protocol=self.protocol).first()
            if existing_port:
                # 端口规则存在，检查是否需要更新
                if existing_port.is_allowed != self.is_allowed or existing_port.description != self.description:
                    existing_port.is_allowed = self.is_allowed
                    existing_port.description = self.description  # 如果需要，也更新描述
                    db.session.commit()
                    # 执行相应的UFW命令
                    result = subprocess.run(command, shell=True, check=False)
                    if result.returncode == 0:
                        return True, "端口规则更新成功"
                    else:
                        return False, "执行ufw命令失败"
                else:
                    # 端口规则已存在且无需更新
                    return True, "端口规则已存在且无需更新"
            else:
                # 端口规则不存在，添加新规则
                new_port = ufw_port(port=self.port, protocol=self.protocol, description=self.description,
                                    is_allowed=self.is_allowed)
                db.session.add(new_port)
                # 执行相应的UFW命令
                result = subprocess.run(command, shell=True, check=False)
                if result.returncode == 0:
                    db.session.commit()
                    return True, "端口添加成功"
                else:
                    db.session.rollback()  # 如果UFW命令执行失败，回滚数据库操作
                    return False, "执行ufw命令失败"
        except IntegrityError as e:
            db.session.rollback()
            return False, f"数据库错误: {str(e)}"
        except Exception as e:
            db.session.rollback()
            return False, f"执行过程中发生错误: {str(e)}"

    @staticmethod
    def delete_port_by_id(rule_id):
        port_obj = ufw_port.query.filter_by(id=rule_id)
        if port_obj.first() is None:
            return False, "端口不存在"
        action = "allow" if port_obj.first().is_allowed else "deny"
        command = f"sudo ufw delete {action} {port_obj.first().port}/{port_obj.first().protocol}"
        result = subprocess.run(command, shell=True, check=False)
        port_obj.delete()
        if result.returncode == 0:
            db.session.commit()
            return True, "端口删除成功"
        else:
            db.session.rollback()
            return False, "执行ufw命令失败"


class IPManager:
    def __init__(self, ip, protocol, description, is_allowed):
        self.ip = ip
        self.protocol = protocol
        self.description = description
        self.is_allowed = is_allowed

    @staticmethod
    def get_ip(page=1, limit=20):
        ip_list = ufw_ip.query.all()
        result = []
        for ip in ip_list:
            result.append({
                "rule_id": ip.id,
                "ip": ip.ip,
                "protocol": ip.protocol,
                "description": ip.description,
                "is_allowed": ip.is_allowed
            })
        return result

    def add_ip(self):
        action = "allow" if self.is_allowed else "deny"
        try:
            # 检查是否存在相同的IP规则
            existing_ip = ufw_ip.query.filter_by(ip=self.ip, protocol=self.protocol).first()
            if existing_ip:
                # 如果存在，检查是否需要更新规则
                if existing_ip.is_allowed != self.is_allowed:
                    existing_ip.is_allowed = self.is_allowed
                    existing_ip.description = self.description  # 如果需要，也更新描述
                    db.session.commit()
                    command = ["sudo", "ufw", action, "from", self.ip, "proto", self.protocol]
                    subprocess.run(command, check=False)
                    return True, "地址规则更新成功"
                else:
                    return True, "地址规则已存在且无需更新"
            else:
                # 添加新的IP规则
                ufw_ip_obj = ufw_ip(ip=self.ip, protocol=self.protocol, description=self.description,
                                    is_allowed=self.is_allowed)
                db.session.add(ufw_ip_obj)
            # 构建并执行UFW命令
            command = ["sudo", "ufw", action, "from", self.ip, "proto", self.protocol]
            result = subprocess.run(command, check=False)
            if result.returncode == 0:
                db.session.commit()
                return True, "地址添加成功"
            else:
                # 如果UFW命令执行失败，回滚数据库操作
                db.session.rollback()
                return False, "执行ufw命令失败"
        except IntegrityError as e:
            db.session.rollback()
            return False, f"数据库错误: {str(e)}"

    @staticmethod
    def delete_ip_by_id(rule_id):
        ip_obj = ufw_ip.query.filter_by(id=rule_id)
        if ip_obj.first() is None:
            return False, "地址不存在"
        action = "allow" if ip_obj.first().is_allowed else "deny"
        command = ["sudo", "ufw", "delete", action, "from", ip_obj.first().ip, "proto", ip_obj.first().protocol]
        result = subprocess.run(command, check=False)
        ip_obj.delete()
        if result.returncode == 0:
            db.session.commit()  # 只有在UFW命令执行成功后才提交数据库更改
            return True, "地址删除成功"
        else:
            db.session.rollback()  # UFW命令执行失败，回滚数据库操作
            return False, "执行ufw命令失败"

