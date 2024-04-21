import contextlib
import json
import os
import subprocess
from typing import List, Dict, Any
from flask import jsonify, Response

from FlaskAppSingleton import FlaskAppSingleton
from models import FileManager
from functions.sql_func import execute
db = FlaskAppSingleton().get_db()


class WebSite(db.Model):
    __tablename__ = 'nginx'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    port = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, port):
        self.id = id
        self.name = name
        self.port = port


web_site = WebSite


class NginxManager:
    BASE_WEBSITE_DIR = "/var/www/nginx/"
    TMP_DIR = "/tmp/"
    SITES_ENABLED_DIR = "/etc/nginx/sites-enabled/"
    RELOAD_COMMAND = "sudo nginx -s reload"

    def __init__(self, name: str):
        self.name = name

    def delete_file(self):
        self._run_command(f"rm -rf {self.BASE_WEBSITE_DIR}{self.name}")
        self._run_command(f"rm -f {self.TMP_DIR}{self.name}.zip")
        self._run_command(f"rm -f {self.SITES_ENABLED_DIR}{self.name}")
        self._reload_nginx()

        try:
            web_site.query.filter_by(name=self.name).delete()
        except Exception as e:
            print(f"Error deleting record from database: {e}")

    def upload(self, file: str, port: int):
        self.delete_file()
        file_manager = FileManager(self.TMP_DIR)
        file_manager.upload(file)

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                log = subprocess.check_output(
                    ['sh', 'scripts/create_website.sh', self.name.replace(".zip", ""), str(port)]
                )
                print(log.decode().strip())

        # try:
        #     execute('INSERT INTO nginx (name, port) VALUES (?, ?)', (self.name, port))
        # except Exception as e:
        #     print(f"Error inserting record into database: {e}")

    @staticmethod
    def get_web_list():
        # 从数据库中获取网站列表
        web_list = web_site.query.all()
        result = []
        for web in web_list:
            result.append({
                "id": web.id,
                "name": web.name,
                "port": web.port
            })
        return result


    def _run_command(self, command: str):
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}\n{e}")

    def _reload_nginx(self):
        try:
            subprocess.check_call(self.RELOAD_COMMAND, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error reloading Nginx: {e}")
