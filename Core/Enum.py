# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Enum(tuple):
    __getattr__ = tuple.index
