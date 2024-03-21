# singleton.py
import threading

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Ensure we are safe from race conditions in multi-threaded environments
            with cls._instances_lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class FlaskAppSingleton(metaclass=SingletonMeta):
    _instances_lock = threading.Lock()

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        db_path_prefix = sys.platform.startswith('win') and 'sqlite:///' or 'sqlite:////'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = db_path_prefix + os.path.join(self.app.root_path, "database.db")
        self.db = SQLAlchemy(self.app)

    def get_app(self):
        return self.app

    def get_db(self):
        return self.db
