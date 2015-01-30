# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *


class MIndicator(QFrame):
    def __init__(self, parent=None):
        super(MIndicator, self).__init__(parent)
        self.__default_font = QFont('Microsoft Yahei', 8, QFont.Normal)
        self.__pic_bg = QPixmap(':resource')
        self.displayer = self.MDisplayer(self)
        self.timer = QTimer(self)
        QObject.connect(self.timer, SIGNAL('timeout()'), self, SLOT('__roll_text()'))
        self.timer.setInterval(1000)
        self.__text = None

    def setText(self, text):
        if QFontMetrics(self.__default_font).width(text) + 8 < self.width():
            self.__text = QString(text)
            if self.timer.isActive():
                self.timer.stop()
        elif not self.timer.isActive():
            self.__text = QString(text + '                  ')
            self.timer.start()
        self.displayer.repaint()

    def getText(self):
        return self.__text

    @pyqtSlot()
    def __roll_text(self):
        self.__text = self.__text.mid(1) + self.__text.left(1)
        self.displayer.repaint()

    def setRollingSpeed(self, int_speed):
        self.timer.setInterval(int_speed)

    def getDefaultFont(self):
        return self.__default_font

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, 10, 23, self.__pic_bg, 25, 70, 10, 23)
        painter.drawPixmap(10, 0, self.width() - 20, 23, self.__pic_bg, 35, 70, 1, 23)
        painter.drawPixmap(self.width() - 10, 0, 10, 23, self.__pic_bg, 36, 70, 10, 23)

    def resizeEvent(self, event):
        self.displayer.setGeometry(4, 1, event.size().width() - 8, 20)


    class MDisplayer(QLabel):
        def __init__(self, parent=None):
            super(MIndicator.MDisplayer, self).__init__(parent)
            self.__parent = parent

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.TextAntialiasing)
            painter.setFont(self.__parent.getDefaultFont())
            painter.setPen(QColor(250, 250, 250, 250))
            painter.drawText(0, 0, self.width(), self.height(), Qt.AlignVCenter | Qt.AlignHCenter,
                             self.__parent.getText())
