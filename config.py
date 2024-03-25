import json


class Config:
    SECRET_KEY = None

    def __init__(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)

        self.SECRET_KEY = self.config['SECRET_KEY']


config = Config('config.json')
