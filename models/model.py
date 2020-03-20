# coding:utf-8
from utils.api import RequestHandler

from utils.custom_thread import CallBackThread


class Model:
    def __init__(self):
        self.api = RequestHandler()
        self.thread = None

    def remove_bg(self, file_path, call_back):
        if self.thread:
            self.thread.exit()
            self.thread.wait()
            self.thread = None
        self.thread = CallBackThread(self.api.remove_bg, file_path)
        self.thread.done_signal.connect(call_back)
        self.thread.start()


def main():
    pass


if __name__ == "__main__":
    main()
