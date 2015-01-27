# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *


class MStyleSetter:
    @staticmethod
    def setStyle(widget, path_stylesheet):
        file_qss = QFile(path_stylesheet)
        file_qss.open(QFile.ReadOnly)
        widget.setStyleSheet(QString(file_qss.readAll()))
