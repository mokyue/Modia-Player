# -*- coding: utf-8 -*-
from PyQt4.QtGui import QFont, QFontMetrics, QPainter, QColor, QLinearGradient, QBrush
from PyQt4.QtCore import Qt
from Widget.MFrame import MFrame
from Core.LyricParser import LyricParser
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class MLyricPanel(MFrame):
    def __init__(self, parent=None):
        super(MLyricPanel, self).__init__(parent)
        self.__default_font = QFont('Microsoft Yahei', 8, QFont.Normal)
        self.__highlight_font = QFont('Microsoft Yahei', 10, QFont.Bold)
        self.__height_default_font = QFontMetrics(self.__default_font).height()
        self.__height_highlight_font = QFontMetrics(self.__highlight_font).height()
        self.__dict_lyric = dict()
        self.__past_lyric = ''
        self.__current_lyric = ''
        self.__coming_lyric = ''
        self.__list_timestamp = list()

    def setLyricFile(self, lrc_path):
        self.__dict_lyric = LyricParser.parse(lrc_path)
        self.__list_timestamp = list()
        for timestamp in self.__dict_lyric:
            self.__list_timestamp.append(timestamp)
        self.__list_timestamp.sort()

    def setNoLyric(self):
        self.__past_lyric = ''
        self.__current_lyric = u'无歌词信息'
        self.__coming_lyric = ''
        self.repaint()

    def switchLyric(self, int_time):
        current_time = int_time / 1000 * 1000
        try:
            index = self.__list_timestamp.index(current_time)
        except ValueError:
            return
        self.__past_lyric = ''
        self.__current_lyric = ''
        self.__coming_lyric = ''
        for i in range(0, index):
            self.__past_lyric += self.__dict_lyric.get(self.__list_timestamp[i])
        self.__current_lyric += self.__dict_lyric.get(self.__list_timestamp[index])
        for i in range(index + 1, len(self.__list_timestamp) - 1):
            self.__coming_lyric += self.__dict_lyric.get(self.__list_timestamp[i])
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setFont(self.__default_font)
        painter.setPen(QColor(60, 60, 60, 255))
        painter.drawText(0, 0, self.width(), self.height() / 2, Qt.AlignHCenter | Qt.AlignBottom, self.__past_lyric)
        painter.drawText(0, self.height() / 2 + self.__height_highlight_font, self.width(), self.height() / 2,
                         Qt.AlignHCenter | Qt.AlignTop, self.__coming_lyric)
        painter.setFont(self.__highlight_font)
        painter.setPen(QColor(0, 0, 0, 255))
        painter.drawText(0, (self.height() - self.__height_highlight_font) / 2, self.width(),
                         self.__height_highlight_font * 2, Qt.AlignHCenter | Qt.AlignVCenter, self.__current_lyric)
        linearGradient = QLinearGradient(0, 0, 0, self.height())
        linearGradient.setColorAt(0, QColor(255, 255, 255, 255))
        linearGradient.setColorAt(0.4, QColor(255, 255, 255, 0))
        linearGradient.setColorAt(0.6, QColor(255, 255, 255, 0))
        linearGradient.setColorAt(1.0, QColor(255, 255, 255, 255))
        painter.setBrush(QBrush(linearGradient))
        painter.drawRect(-1, -1, self.width() + 2, self.height() + 2)
