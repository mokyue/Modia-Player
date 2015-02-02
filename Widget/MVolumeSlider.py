# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from PyQt4.QtCore import Qt
from PyQt4.phonon import Phonon
from Core.MStyleSetter import MStyleSetter


class MVolumeSlider(Phonon.VolumeSlider):
    def __init__(self, parent=None):
        super(MVolumeSlider, self).__init__(parent)
        self.setMouseTracking(True)
        MStyleSetter.setStyle(self, ':qss_sld_music_volume')
        self.setCursor(Qt.PointingHandCursor)
