# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from Form.ModiaWindow import *


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
