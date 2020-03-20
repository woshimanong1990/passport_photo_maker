# coding:utf-8
from PyQt5.QtCore import QObject, pyqtSignal
from models.model import Model


class Present(QObject):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = Model()

    def remove_bg_call_back(self, result):
        """
        这个做法不太妥当，应该是促发信号
        """
        if isinstance(result, Exception):
            self.view.show_error(str(result))
            return
        self.view.show_remove_result(result)

    def remove_bg(self, file_path):
        self.model.remove_bg(file_path, self.remove_bg_call_back)


def main():
    pass


if __name__ == "__main__":
    main()
