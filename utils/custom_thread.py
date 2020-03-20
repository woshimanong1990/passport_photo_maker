# coding:utf-8

from PyQt5.QtCore import QThread, pyqtSignal
from utils.variables import LOGGER


class CallBackThread(QThread):
    done_signal = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.done_signal.emit(result)
        except Exception as e:
            LOGGER.error("run error", exc_info=True)
            self.done_signal.emit(e)

def main():
    pass


if __name__ == "__main__":
    main()
