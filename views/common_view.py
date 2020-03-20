# -*- coding: utf-8 -*-
import time
from PyQt5.QtWidgets import QSplashScreen, QApplication, QWidget, QMessageBox, QSpacerItem, QSizePolicy, QGridLayout
from PyQt5.QtGui import QPixmap, QMovie, QPainter
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import res.loading


class MovieSplashScreen(QSplashScreen):

    def __init__(self, movie, flags, parent=None):
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())

        QSplashScreen.__init__(self, pixmap, flags)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


class CommonView(QWidget):
    update_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CommonView, self).__init__(parent=parent)
        self._watch_config = {}
        self._signal_wrapper = []
        self.update_signal.connect(self.update_watch_value)



    def closeEvent(self, *args, **kwargs):
        super(CommonView, self).closeEvent(*args, **kwargs)

    def init_env(self):
        pass

    def update_watch_value(self, key):
        depend_list = self._watch_config.get(key, [])
        for call_back in depend_list:
            call_back()

    def watch_config(self, attr, call_back):
        if not callable(call_back):
            raise Exception("call_back is not callable")
        depend_list = self._watch_config.setdefault(attr, [])
        depend_list.append(call_back)

    def __setattr__(self, key, value):
        super(CommonView, self).__setattr__(key, value)
        config = getattr(self, '_watch_config', None)
        if config is None or key == '_watch_config':
            return
        depend_list = self._watch_config.get(key, [])
        if depend_list:
            self.update_signal.emit(key)


class LoadingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.loading = None

    def show_loading(self):
        screen = QApplication.desktop().screenNumber(self)
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        self.loading = MovieSplashScreen(QMovie(':/123/images/810.gif'), Qt.WindowStaysOnTopHint)
        # 移动到当前活动窗口的正中央
        frameGm = self.loading.frameGeometry()
        frameGm.moveCenter(centerPoint)
        self.loading.move(frameGm.topLeft())
        self.loading.show()

    def finish_loading(self):
        if hasattr(self, "loading") and self.loading:
            self.loading.finish(self.parent())