# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import os
import sys

import logging
from logging.handlers import RotatingFileHandler


_LOGGER = logging.getLogger()


def setup_logger(file_name):
    """
    日志配置
    :param file_name:
    :return:
    """
    log_file = os.path.join(os.path.expanduser('~'), file_name)
    log_config_dict = {}
    fmt = "%(levelname)s,%(name)s %(asctime)s %(module)s,%(lineno)s %(message)s"
    # todo:debug
    level = "WARNING"
    log_config_dict[
        "format"] = fmt
    log_config_dict["level"] = level
    logging.basicConfig(**log_config_dict)
    _LOGGER.debug('get log config dict %s', log_config_dict)

    file_rotaing_handler = RotatingFileHandler(
        filename=log_file,
        backupCount=10,
        maxBytes=1024 * 1024 * 50,
    )
    file_rotaing_handler.setLevel(level)
    formatter = logging.Formatter(fmt)
    file_rotaing_handler.setFormatter(formatter)
    _LOGGER.addHandler(file_rotaing_handler)


def main():
    pass


if __name__ == "__main__":
    main()
