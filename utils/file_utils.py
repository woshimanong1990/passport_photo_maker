# coding:utf-8
import os
import sys
import json
from utils.variables import LOGGER

def get_root_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_settings_data():
    try:
        root_dir = get_root_dir()
        if getattr(sys, 'frozen', False):
            settings_path = os.path.join(root_dir, 'settings.json')
        else:
            settings_path = os.path.join(root_dir, "data/settings.json")
        with open(settings_path, "r") as f:
            return json.load(f)
    except:
        LOGGER.error("get setting data error")
        return {}


def get_api_public_key():
    try:
        data = get_settings_data()
        return data["X-Api-Key"]
    except:
        LOGGER.error("get public key error")


def get_request_timeout():
    try:
        data = get_settings_data()
        return data["timeout"]
    except:
        LOGGER.error("get public key error")


def main():
    pass


if __name__ == "__main__":
    main()
