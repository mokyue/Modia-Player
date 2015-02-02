# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from PyQt4.QtCore import QTime, Qt, QString
from PyQt4.QtGui import QMessageBox, QTableWidgetItem, QFileDialog, QDesktopServices
from PyQt4.phonon import Phonon
from Widget.MButton import MButton
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class AudioManager():
    def __init__(self, window, lyric_panel):
        self.__main_window = window
        self.__lyric_panel = lyric_panel
        self.__audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self.__main_window)
        self.__media_object = Phonon.MediaObject(self.__main_window)
        self.__media_object.setTickInterval(1000)
        self.__media_object.tick.connect(self.tick)
        self.__media_object.stateChanged.connect(self.stateChanged)
        self.__media_object.currentSourceChanged.connect(self.currentSourceChanged)
        self.__media_object.aboutToFinish.connect(self.aboutToFinish)
        self.__meta_information_resolver = Phonon.MediaObject(self.__main_window)
        self.__meta_information_resolver.stateChanged.connect(self.metaStateChanged)
        self.__music_table = self.__main_window.getMusicTable()
        self.__list_music = list()
        Phonon.createPath(self.__media_object, self.__audio_output)
        self.__register_ui()

    def __register_ui(self):
        self.__main_window.getActionBar().get_widget('SLD_VOL').setAudioOutput(self.__audio_output)
        self.__main_window.getActionBar().get_widget('SLD_SEEK').setMediaObject(self.__media_object)

    def tick(self, time):
        self.__main_window.getActionBar().get_widget('LBL_TIME_REMAIN').setText(
            QTime(0, (time / 60000) % 60, (time / 1000) % 60).toString('mm:ss'))
        self.__lyric_panel.switchLyric(time)

    def play(self, media_source=None):
        if media_source != None:
            if not isinstance(media_source, Phonon.MediaSource):
                raise ValueError('Given argument not Phonon.MediaSource type. (Phonon.MediaSource type required)')
            else:
                self.__media_object.setCurrentSource(media_source)
        if len(self.__list_music) < 1:
            self.addMusic()
            if len(self.__list_music) > 0:
                self.__media_object.setCurrentSource(self.__list_music[len(self.__list_music) - 1])
        self.__media_object.play()

    def pause(self):
        self.__media_object.pause()

    def stop(self):
        self.__media_object.stop()

    def next(self):
        index_next = self.__list_music.index(self.__media_object.currentSource()) + 1
        if index_next < len(self.__list_music):
            self.play(self.__list_music[index_next])
        else:
            self.play(self.__list_music[0])

    def previous(self):
        index_previous = self.__list_music.index(self.__media_object.currentSource()) - 1
        if index_previous > -1:
            self.play(self.__list_music[index_previous])
        else:
            self.play(self.__list_music[len(self.__list_music) - 1])

    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.__media_object.errorType() == Phonon.FatalError:
                QMessageBox.warning(self.__main_window, "Fatal Error", self.__media_object.errorString())
                self.__media_object.setCurrentSource(self.__list_music[0])
                self.__list_music.remove(self.__media_object.currentSource())
            else:
                QMessageBox.warning(self.__main_window, "Error", self.__media_object.errorString())
                self.__media_object.setCurrentSource(self.__list_music[0])
                self.__list_music.remove(self.__media_object.currentSource())
        elif newState == Phonon.PlayingState:
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setMStyle(MButton.Type.Pause)
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setToolTip('暂停')
            self.__main_window.setSuspendStatus(False)
            if self.__media_object.isSeekable():
                self.__main_window.getActionBar().get_widget('SLD_SEEK').setCursor(Qt.PointingHandCursor)
            self.__main_window.getActionBar().get_widget('INDICT_INFO').setText(self.__get_music_display_info())
            time_total = self.__media_object.totalTime()
            self.__main_window.getActionBar().get_widget('LBL_TIME_TOTAL').setText(
                QTime(0, (time_total / 60000) % 60, (time_total / 1000) % 60).toString('mm:ss'))
            btn_music_stop = self.__main_window.getActionBar().get_widget('BTN_STOP')
            if not btn_music_stop.isEnabled():
                btn_music_stop.setEnabled(True)
            self.__set_lyric(self.__media_object.currentSource().fileName())
        elif newState == Phonon.StoppedState:
            self.__main_window.getActionBar().get_widget('SLD_SEEK').setCursor(Qt.ArrowCursor)
            self.__main_window.getActionBar().get_widget('INDICT_INFO').setText(u'无音乐')
            self.__main_window.getActionBar().get_widget('LBL_TIME_TOTAL').setText('00:00')
            btn_music_stop = self.__main_window.getActionBar().get_widget('BTN_STOP')
            if btn_music_stop.isEnabled():
                btn_music_stop.setEnabled(False)
            self.__lyric_panel.setNoLyric()
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setMStyle(MButton.Type.Play)
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setToolTip('播放')
            self.__main_window.setSuspendStatus(True)
        elif newState == Phonon.PausedState:
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setMStyle(MButton.Type.Play)
            self.__main_window.getActionBar().get_widget('BTN_PLAY_PAUSE').setToolTip('播放')
            self.__main_window.setSuspendStatus(True)
        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return

    def __set_lyric(self, music_path):
        lrc_path = str(music_path.left(music_path.lastIndexOf('.'))) + u'.lrc'
        if os.path.exists(lrc_path):
            self.__lyric_panel.setLyricFile(lrc_path)
        else:
            self.__lyric_panel.setNoLyric()

    def __get_music_display_info(self):
        metadata = self.__media_object.metaData()
        str_title = metadata.get(QString('TITLE'), [''])[0]
        if str_title != '':
            str_indicator = str(str_title)
        else:
            str_indicator = str(self.__media_object.currentSource().fileName())
        str_artist = metadata.get(QString('ARTIST'), [''])[0]
        if str_artist != '':
            str_indicator += ' - '
            str_indicator += str(str_artist)
        str_description = metadata.get(QString('DESCRIPTION'), [''])[0]
        if str_description != '':
            str_indicator += '   '
            str_indicator += str(str_description)
        return str_indicator

    def metaStateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            QMessageBox.warning(self.__main_window, "Error opening files",
                                self.__meta_information_resolver.errorString())
            while self.__list_music and self.__list_music.pop() != self.__meta_information_resolver.currentSource():
                pass
            return
        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return
        if self.__meta_information_resolver.currentSource().type() == Phonon.MediaSource.Invalid:
            return
        metaData = self.__meta_information_resolver.metaData()
        title = metaData.get(QString('TITLE'), [''])[0]
        if not title:
            title = self.__meta_information_resolver.currentSource().fileName()
        artist = metaData.get(QString('ARTIST'), [''])[0]
        if artist:
            title = title + ' - ' + artist
        titleItem = QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        long_duration = self.__meta_information_resolver.totalTime()
        total_time_item = QTableWidgetItem(
            QTime(0, (long_duration / 60000) % 60, (long_duration / 1000) % 60).toString('mm:ss'))
        total_time_item.setFlags(total_time_item.flags() ^ Qt.ItemIsEditable)
        total_time_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        currentRow = self.__music_table.rowCount()
        self.__music_table.insertRow(currentRow)
        self.__music_table.setItem(currentRow, 0, titleItem)
        self.__music_table.setItem(currentRow, 1, total_time_item)
        if not self.__music_table.selectedItems():
            self.__music_table.selectRow(0)
            self.__media_object.setCurrentSource(self.__meta_information_resolver.currentSource())
        index = self.__list_music.index(self.__meta_information_resolver.currentSource()) + 1
        if len(self.__list_music) > index:
            self.__meta_information_resolver.setCurrentSource(self.__list_music[index])

    def currentSourceChanged(self, source):
        self.__music_table.selectRow(self.__list_music.index(source))

    def aboutToFinish(self):
        index_next = self.__list_music.index(self.__media_object.currentSource()) + 1
        if index_next < len(self.__list_music):
            self.__media_object.enqueue(self.__list_music[index_next])
        else:
            self.__media_object.enqueue(self.__list_music[0])

    def addMusic(self):
        if len(self.__list_music) < 1:
            is_empty = True
        else:
            is_empty = False
        sources = QFileDialog.getOpenFileNames(self.__main_window, "Select Music Files",
                                               QDesktopServices.storageLocation(QDesktopServices.MusicLocation))
        if not sources:
            return
        index = len(self.__list_music)
        for music_file in sources:
            media_source = Phonon.MediaSource(music_file)
            if not self.__is_existing(media_source):
                self.__list_music.append(media_source)
        if is_empty:
            self.__media_object.setCurrentSource(self.__list_music[len(self.__list_music) - 1])
        if index == len(self.__list_music):
            return
        if self.__list_music:
            self.__meta_information_resolver.setCurrentSource(self.__list_music[index])

    def __is_existing(self, media_source):
        for ms in self.__list_music:
            if media_source.fileName() == ms.fileName():
                return True
        return False

    def clearQueue(self):
        self.__media_object.clearQueue()

    def setCurrentSourceByIndex(self, int_index):
        self.__media_object.setCurrentSource(self.__list_music[int_index])

    def getMediaObjectState(self):
        return self.__media_object.state()
