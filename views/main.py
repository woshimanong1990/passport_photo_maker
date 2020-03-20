# coding:utf-8
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from ui_files.UI_main import Ui_MainWindow
from utils.photo_utils import bytes_to_qimage, design_photo, pilow_image_to_qt_pixmap, bytes_to_pillow_image, \
    pil2pixmap, fill_background_color
from views.common_view import LoadingView
from presents.present import Present
from utils.view_utils import error_capture
from views.image_preview import PreviewDialog
from views.show_message_dialog import MyDialog
from utils.variables import COLOR_MAP, SIZE_MAP


class MainWindow(QMainWindow, LoadingView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.select_file_path = None
        self.save_file_path = None
        self.present = Present(self)
        self.image_bytes = None
        self.dialog = None
        self.color = (0, 191, 243)
        self.size = 's1x5'
        self.design_bg_image = None
        self.remove_bg_image = None
        self.pix_img = None
        self.design_photo_save_path = None
        self.is_no_remove = False

    @error_capture()
    def aboutAction(self, *args, **kwargs):
        dialog = MyDialog("""一个爱折腾的pythoner\n\n微信公众号：python码码有趣的\n\nqq群：389954854""")
        dialog.exec()

    @error_capture()
    def declareAction(self, *args, **kwargs):
        dialog = MyDialog("本软件仅供交流学习，请勿商用。\n\n软件是对https://www.remove.bg/的简单的封装，抠图效果因人而异。")
        dialog.exec()

    @error_capture()
    def helpAction(self, *args, **kwargs):
        dialog = MyDialog("1:配置软件目录下的settings.json（自行申请public key）\n\n2: 选择图片，点击抠图。可能比较需要点时间\n\n"
                          "3：查看图片可以放大图片\n\n")
        dialog.exec()

    def mock_data(self):
        with open(r"E:\tmp\download\dog.jpg", 'rb') as f:
            self.image_bytes = f.read()

    @error_capture(need_info=True)
    def colorSelectAction(self, index):
        if not self.remove_bg_image:
            QMessageBox.critical(None, "错误", "没有抠图")
            return
        if index == -2:
            self.color = (0, 191, 243)
        else:
            self.color = (255, 0, 0)
        self.show_design_photo()

    @error_capture()
    def selectPhotoAction(self, *args, **kwargs):
        file_path, _ = QFileDialog.getOpenFileName(None, "请选择图片", "", "imges(*.jpeg *.jpg *.png)")
        if not file_path:
            QMessageBox.critical(None, "错误", "请选择图片")
            return
        self.select_file_path = file_path
        pixmap = QPixmap(self.select_file_path)
        self.ui.removeBGLabel.clear()
        self.remove_bg_image = None
        self.design_bg_image = None
        self.ui.originLabel.setPixmap(pixmap.scaled(self.ui.originLabel.size(), QtCore.Qt.KeepAspectRatio))
        if self.is_no_remove:
            self.remove_bg_image = Image.open(self.select_file_path)
            self.show_design_photo()


    @error_capture(need_info=True)
    def removeBackgroundAction(self, *args, **kwargs):
        """
        异步调用，实际上是由一个线程做的。回调触发一个信息后，交由主线程处理
        """
        if not self.select_file_path:
            QMessageBox.critical(None, "错误", "请选择图片")
            return
        self.show_loading()
        self.present.remove_bg(self.select_file_path)
        # self.mock_data()
        # self.show_remove_result(self.image_bytes)

    @error_capture(need_info=True)
    def amplifyAction(self, *args, **kwargs):
        """
        不仅仅是放大图片，主要是旋转，放大缩小
        """
        if not self.image_bytes:
            QMessageBox.critical(None, "错误", "没有抠图图片")
            return
        self.dialog = PreviewDialog(self.image_bytes)
        self.dialog.exec()

    @error_capture(need_info=True)
    def saveRemoveResultAction(self, *args, **kwargs):
        if not self.remove_bg_image:
            QMessageBox.critical(None, "错误", "没有抠图")
            return
        file_path, _ = QFileDialog.getSaveFileName(None, "请选择保存路径", "", "imges(*.png)")
        if not file_path:
            QMessageBox.critical(None, "错误", "请选择图片")
            return
        self.remove_bg_image.save(file_path)

    @error_capture(need_info=True)
    def saveDesignResultAction(self, *args, **kwargs):
        if not self.remove_bg_image:
            QMessageBox.critical(None, "错误", "没有抠图")
            return
        if not self.design_bg_image:
            QMessageBox.critical(None, "错误", "没有排版图片")
            return
        file_path, _ = QFileDialog.getSaveFileName(None, "请选择保存路径", "", "imges(*.jpeg *.jpg *.png)")
        if not file_path:
            QMessageBox.critical(None, "错误", "请选择图片")
            return
        self.design_bg_image.save(file_path)
        self.design_photo_save_path = file_path
        self.ui.openPushButton.setEnabled(True)

    @error_capture(need_info=True)
    def openSaveAction(self, *args, **kwargs):
        """
        打开图片
        """
        if not self.design_photo_save_path or not os.path.isfile(self.design_photo_save_path):
            QMessageBox.critical(None, "错误", "没有排版图片或者已删除")
            return
        os.startfile(self.design_photo_save_path)

    def show_design_photo(self):
        image = fill_background_color(self.remove_bg_image, self.color)
        self.design_bg_image = design_photo(image, self.size)
        self.pix_img = pil2pixmap(self.design_bg_image)
        size = self.ui.IndesignLabel.size()
        self.ui.IndesignLabel.setPixmap(self.pix_img.scaled(size.width(), size.height(), QtCore.Qt.KeepAspectRatio))

    @error_capture(need_info=True)
    def sizeSelectAction(self, index):
        if not self.remove_bg_image:
            QMessageBox.critical(None, "错误", "没有抠图")
            return
        self.size = SIZE_MAP[index][0]
        self.show_design_photo()

    @error_capture()
    def show_error(self, message):
        self.finish_loading()
        QMessageBox.critical(None, "错误", message)

    @error_capture(need_info=True)
    def show_remove_result(self, result):
        self.finish_loading()
        self.image_bytes = result
        image = bytes_to_qimage(result)
        self.remove_bg_image = bytes_to_pillow_image(result)
        size = self.ui.removeBGLabel.size()
        self.ui.removeBGLabel.setPixmap(QPixmap.fromImage(image.scaled(size, QtCore.Qt.KeepAspectRatio)))
        self.show_design_photo()

    @error_capture(need_info=True)
    def noRemoveAction(self, is_no_remove):
        self.is_no_remove = is_no_remove
        is_enabled = not is_no_remove
        self.ui.removeButton.setEnabled(is_enabled)
        self.ui.previewPushButton.setEnabled(is_enabled)
        self.ui.saveResultpushButton.setEnabled(is_enabled)






def main():
    pass


if __name__ == "__main__":
    main()
