# -*- coding: utf-8 -*-
from PyQt4.QtCore import QFile, QString
from Resource.modia_rc import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class MStyleSetter:
    @staticmethod
    def setStyle(widget, path_stylesheet):
        file_qss = QFile(path_stylesheet)
        file_qss.open(QFile.ReadOnly)
        widget.setStyleSheet(QString(file_qss.readAll()))
        file_qss.close()
