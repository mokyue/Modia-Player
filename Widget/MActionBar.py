# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *
from MButton import MButton


class MActionBar(QFrame):
    def __init__(self, parent=None):
        super(MActionBar, self).__init__(parent)
        self.__dict_widget = dict()
        self.__setup_ui()

    def __setup_ui(self):
        btn_music_previous = MButton(self, MButton.Type.Previous)
        btn_music_previous.setGeometry(13, 13, 28, 29)
        btn_music_previous.setToolTip('上一首')
        self.__dict_widget['BTN_PREVIOUS'] = btn_music_previous
        btn_music_next = MButton(self, MButton.Type.Next)
        btn_music_next.setGeometry(69, 13, 28, 29)
        btn_music_next.setToolTip('下一首')
        self.__dict_widget['BTN_NEXT'] = btn_music_next
        btn_music_play_pause = MButton(self, MButton.Type.Play)
        btn_music_play_pause.setGeometry(38, 10, 34, 35)
        btn_music_play_pause.setToolTip('播放')
        self.__dict_widget['BTN_PLAY_PAUSE'] = btn_music_play_pause
        btn_music_stop = MButton(self, MButton.Type.Stop)
        btn_music_stop.setGeometry(94, 13, 28, 29)
        btn_music_stop.setToolTip('停止')
        self.__dict_widget['BTN_STOP'] = btn_music_stop
        volume_slider = Phonon.VolumeSlider(self)
        volume_slider.setGeometry(130, 18, 100, 18)
        self.__dict_widget['SLD_VOL'] = volume_slider

    def get_widget(self, key):
        return self.__dict_widget[key]
