# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.ui'):
            os.system('pyuic4 -o ui_%s.py %s' % (file.rsplit('.', 1)[0], root + '\\' + file))
        elif file.endswith('.qrc'):
            os.system('pyrcc4 -o %s_rc.py %s' % (file.rsplit('.', 1)[0], root + '\\' + file))