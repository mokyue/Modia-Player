# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from PyQt4.QtGui import QFrame
from PyQt4.QtCore import Qt
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class MFrame(QFrame):
    def __init__(self, parent=None):
        super(MFrame, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.cursor() != Qt.ArrowCursor:
            self.setCursor(Qt.ArrowCursor)
