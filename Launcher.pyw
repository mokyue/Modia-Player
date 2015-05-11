# -*- coding: utf-8 -*-
from PyQt4.QtCore import QTextCodec
from PyQt4.QtGui import QApplication
from Form.ModiaWindow import ModiaWindow
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = QApplication(sys.argv)
app.setApplicationName("Modia Player")
app.setQuitOnLastWindowClosed(True)
codec = QTextCodec.codecForName('UTF-8')
QTextCodec.setCodecForTr(codec)
QTextCodec.setCodecForLocale(codec)
QTextCodec.setCodecForCStrings(codec)
window = ModiaWindow()
window.show()
sys.exit(app.exec_())
