import os
import configparser


def load_configs(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    default = {**dict(config.items("server")), **dict(config.items("db"))}

    for key in default.keys():
        os.environ.setdefault(key.upper(), default[key])


def get(key: str):
    return os.environ.get(key)
