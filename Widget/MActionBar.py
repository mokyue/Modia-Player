# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *
from MButton import MButton
from MIndicator import MIndicator
from MFrame import MFrame


class MActionBar(MFrame):
    def __init__(self, parent=None):
        super(MActionBar, self).__init__(parent)
        self.__pic_bg = QPixmap(':resource')
        self.__dict_widget = dict()
        self.__setup_ui()

    def __setup_ui(self):
        self.__btn_music_previous = MButton(self, MButton.Type.Previous)
        self.__btn_music_previous.setToolTip('上一首')
        self.__dict_widget['BTN_PREVIOUS'] = self.__btn_music_previous
        self.__btn_music_next = MButton(self, MButton.Type.Next)
        self.__btn_music_next.setToolTip('下一首')
        self.__dict_widget['BTN_NEXT'] = self.__btn_music_next
        self.__btn_music_play_pause = MButton(self, MButton.Type.Play)
        self.__btn_music_play_pause.setToolTip('播放')
        self.__dict_widget['BTN_PLAY_PAUSE'] = self.__btn_music_play_pause
        self.__btn_music_stop = MButton(self, MButton.Type.Stop)
        self.__btn_music_stop.setToolTip('停止')
        self.__btn_music_stop.setEnabled(False)
        self.__dict_widget['BTN_STOP'] = self.__btn_music_stop
        self.__indicator = MIndicator(self)
        self.__indicator.setText('No music')
        self.__indicator.setRollingSpeed(300)
        self.__dict_widget['INDICT_INFO'] = self.__indicator
        self.__volume_slider = Phonon.VolumeSlider(self)
        MStyleSetter.setStyle(self.__volume_slider, ':qss_sld_music_volume')
        self.__volume_slider.setCursor(Qt.PointingHandCursor)
        self.__dict_widget['SLD_VOL'] = self.__volume_slider
        self.__seek_slider = Phonon.SeekSlider(self)
        MStyleSetter.setStyle(self.__seek_slider, ':qss_sld_music_seek')
        self.__dict_widget['SLD_SEEK'] = self.__seek_slider
        self.__label_time_remain = QLabel(self)
        self.__label_time_remain.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        MStyleSetter.setStyle(self.__label_time_remain, ':qss_lbl_time_remain')
        self.__label_time_remain.setText('00:00')
        self.__dict_widget['LBL_TIME_REMAIN'] = self.__label_time_remain
        self.__label_time_total = QLabel(self)
        self.__label_time_total.setAlignment(Qt.AlignRight | Qt.AlignTop)
        MStyleSetter.setStyle(self.__label_time_total, ':qss_lbl_time_remain')
        self.__label_time_total.setText('00:00')
        self.__dict_widget['LBL_TIME_TOTAL'] = self.__label_time_total
        self.__btn_lyric = QPushButton(self)
        self.__btn_lyric.setToolTip('歌词')
        self.__dict_widget['BTN_LYRIC'] = self.__btn_lyric
        self.__btn_add_music = QPushButton(self)
        self.__btn_add_music.setToolTip('添加音乐')
        self.__dict_widget['BTN_ADD_MUSIC'] = self.__btn_add_music

    def get_widget(self, key):
        return self.__dict_widget[key]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height() - 8, self.__pic_bg, 12, 28, 1, 54)
        painter.drawPixmap(0, self.height() - 8, self.width(), 8, self.__pic_bg, 12, 82, 1, 8)

    def resizeEvent(self, event):
        self.__indicator.setGeometry(16, 16, self.width() - 32, 23)
        self.__seek_slider.setGeometry(self.__indicator.x() - 20, self.__indicator.y() + 38, self.width() + 6, 3)
        self.__label_time_remain.setGeometry(self.__seek_slider.x() + 12, self.__seek_slider.y() + 4, 65, 15)
        self.__label_time_total.setGeometry(self.__label_time_remain.x() + self.__seek_slider.width() - 88,
                                            self.__label_time_remain.y(), self.__label_time_remain.width(),
                                            self.__label_time_remain.height())
        self.__btn_music_previous.setGeometry(self.width() / 2 - 54, self.__indicator.y() + 65, 28, 29)
        self.__btn_music_next.setGeometry(self.__btn_music_previous.x() + 56, self.__btn_music_previous.y(),
                                          self.__btn_music_previous.width(), self.__btn_music_previous.height())
        self.__btn_music_play_pause.setGeometry(self.__btn_music_previous.x() + 25, self.__btn_music_previous.y() - 3,
                                                34, 35)
        self.__btn_music_stop.setGeometry(self.__btn_music_previous.x() + 81, self.__btn_music_previous.y(),
                                          self.__btn_music_previous.width(), self.__btn_music_previous.height())
        self.__volume_slider.setGeometry(self.__btn_music_previous.x() + 120, self.__btn_music_previous.y() + 5, 100,
                                         18)
        self.__btn_lyric.setGeometry(self.__seek_slider.x() + 50, self.__seek_slider.y() + 40, 20, 20)
        self.__btn_add_music.setGeometry(self.__seek_slider.x() + 70, self.__seek_slider.y() + 40, 20, 20)
