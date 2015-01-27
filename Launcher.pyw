# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

import sys
from Form.ModiaWindow import *


app = QApplication(sys.argv)
app.setApplicationName("Modia Player")
app.setQuitOnLastWindowClosed(True)
window = ModiaWindow()
window.show()
sys.exit(app.exec_())
