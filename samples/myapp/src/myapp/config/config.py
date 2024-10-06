import configparser
import os

CONFIG_FILE = os.environ.get("CONFIG_FILE", "/etc/myapp/myapp.conf")


def get_logger():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config["logger"]


def get_database():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config["database"]
