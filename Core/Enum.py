# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Enum(tuple):
    __getattr__ = tuple.index
