# coding:utf-8
from PyQt5.QtWidgets import QMessageBox
from utils.variables import LOGGER


def button_temp_disable(func):
    def wrapped(self, *args, **kwargs):
        sender = self.sender()
        try:
            sender.setEnabled(False)
            func(self, *args, **kwargs)
        finally:
            sender.setEnabled(True)
    return wrapped


def error_capture(need_info=False):
    def wrapper(func):
        def wrapped(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if need_info:
                    QMessageBox.critical(None, "错误", "出错了, %s" % str(e))
                LOGGER.error("%s run error", func.__name__, exc_info=True)
        return wrapped
    return wrapper


def main():
    def t():
        print(t.__name__)
    t()

if __name__ == "__main__":
    main()
