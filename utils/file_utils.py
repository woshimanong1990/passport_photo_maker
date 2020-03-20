# coding:utf-8
import os
import sys
import json
from utils.variables import LOGGER


def get_api_public_key():
    try:
        if getattr(sys, 'frozen', False):
            settings_path = os.path.join(os.path.dirname(sys.executable), 'settings.json')
        else:
            settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      "data/settings.json")
        with open(settings_path, "r") as f:
            return json.load(f)["X-Api-Key"]
    except:
        LOGGER.error("get public key error")


def main():
    pass


if __name__ == "__main__":
    main()
