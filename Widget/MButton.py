# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *


class MButton(QPushButton):
    Type = Enum(['Close', 'Maximize', 'Minimize', 'Restore', 'Previous', 'Play', 'Pause', 'Next', 'Stop'])

    __dict_type = {Type.Close: ':qss_btn_title_close', Type.Maximize: ':qss_btn_title_maximize',
                   Type.Minimize: ':qss_btn_title_minimize', Type.Restore: ':qss_btn_title_restore',
                   Type.Previous: ':qss_btn_music_previous', Type.Play: ':qss_btn_music_play',
                   Type.Pause: ':qss_btn_music_pause', Type.Next: ':qss_btn_music_next',
                   Type.Stop: ':qss_btn_music_stop'}

    def __init__(self, parent=None, b_type=Type.Close):
        super(MButton, self).__init__(parent)
        self.setMStyle(b_type)

    def setMStyle(self, b_type):
        MStyleSetter.setStyle(self, self.__dict_type[b_type])
