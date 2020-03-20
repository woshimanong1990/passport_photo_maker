# coding:utf-8
from PyQt5.QtWidgets import QDialog
from ui_files.UI_show_message import Ui_Dialog


class MyDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.textEdit.clear()
        self.ui.textEdit.setText(str(message))


def main():
    pass


if __name__ == "__main__":
    main()
