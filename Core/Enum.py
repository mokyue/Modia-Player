# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

class Enum(tuple):
    __getattr__ = tuple.index
