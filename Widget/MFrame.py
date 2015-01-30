# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *


class MFrame(QFrame):
    def __init__(self, parent=None):
        super(MFrame, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.cursor() != Qt.ArrowCursor:
            self.setCursor(Qt.ArrowCursor)
