# -*- coding: utf-8 -*-
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import Qt
from Core.Enum import Enum
from Core.MStyleSetter import MStyleSetter
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class MButton(QPushButton):
    Type = Enum(
        ['Close', 'Maximize', 'Minimize', 'Restore', 'Previous', 'Play', 'Pause', 'Next', 'Stop', 'Add_Music',
         'Show_Lyric', 'Hide_Lyric'])

    __dict_type = {Type.Close: ':qss_btn_title_close', Type.Maximize: ':qss_btn_title_maximize',
                   Type.Minimize: ':qss_btn_title_minimize', Type.Restore: ':qss_btn_title_restore',
                   Type.Previous: ':qss_btn_music_previous', Type.Play: ':qss_btn_music_play',
                   Type.Pause: ':qss_btn_music_pause', Type.Next: ':qss_btn_music_next',
                   Type.Stop: ':qss_btn_music_stop', Type.Add_Music: ':qss_btn_add_music',
                   Type.Show_Lyric: ':qss_btn_show_lyric', Type.Hide_Lyric: ':qss_btn_hide_lyric'}

    def __init__(self, parent=None, b_type=Type.Close):
        super(MButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setMStyle(b_type)
        self.setCursor(Qt.PointingHandCursor)

    def setMStyle(self, b_type):
        MStyleSetter.setStyle(self, self.__dict_type[b_type])
