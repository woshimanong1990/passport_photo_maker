# coding:utf-8
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from utils.photo_utils import bytes_to_qimage
from utils.view_utils import error_capture
from ui_files.UI_preview import Ui_Dialog


class PreviewDialog(QDialog):
    def __init__(self, image_data, parent=None):
        super().__init__(parent=parent)
        self.image_data = image_data
        self.q_image = None
        self.rotate = 0
        self.scale = 1
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_image()

    @error_capture()
    def init_image(self, *args, **kwargs):
        self.q_image = bytes_to_qimage(self.image_data)
        self.ui.label.setPixmap(QPixmap.fromImage(self.q_image))

    def transform_image_and_show(self):
        transform = QtGui.QTransform()
        transform.scale(self.scale, self.scale)
        transform.rotate(self.rotate)
        q_image = self.q_image.transformed(transform)
        self.ui.label.setPixmap(QPixmap.fromImage(q_image))

    @error_capture(need_info=True)
    def clockwiseRotateAction(self, *args, **kwargs):
        self.rotate += 90
        self.transform_image_and_show()

    @error_capture(need_info=True)
    def counterClockwiseRotateAction(self, *args, **kwargs):
        self.rotate -= 90
        self.transform_image_and_show()

    @error_capture(need_info=True)
    def zoomInAction(self, *args, **kwargs):
        self.scale += 0.2
        self.transform_image_and_show()

    @error_capture(need_info=True)
    def zomOutAction(self, *args, **kwargs):
        self.scale -= 0.2
        if self.scale < 0.2:
            self.scale = 0.2
        self.transform_image_and_show()


def main():
    pass


if __name__ == "__main__":
    main()
