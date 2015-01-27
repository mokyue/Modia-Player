# -*- coding: utf-8 -*-
__author__ = 'n1213 <myn1213@corp.netease.com>'

from __init__ import *


class AudioManager():
    def __init__(self, window):
        self.__main_window = window
        self.__audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self.__main_window)
        self.mediaObject = Phonon.MediaObject(self.__main_window)
        self.mediaObject.setTickInterval(1000)
        self.mediaObject.tick.connect(self.tick)
        # self.mediaObject.stateChanged.connect(self.stateChanged)
        # self.mediaObject.currentSourceChanged.connect(self.sourceChanged)
        # self.mediaObject.aboutToFinish.connect(self.aboutToFinish)
        # self.metaInformationResolver = Phonon.MediaObject(self)
        # self.metaInformationResolver.stateChanged.connect(self.metaStateChanged)
        # Phonon.createPath(self.mediaObject, self.__audio_output)

    def tick(self, time):
        print(time)
        # self.timeLcd.display(QTime(0, (time / 60000) % 60, (time / 1000) % 60).toString('mm:ss'))

    # def stateChanged(self, new_state, old_state):
    # if new_state == Phonon.ErrorState:
    # if self.mediaObject.errorType() == Phonon.FatalError:
    # QMessageBox.warning(self.__main_window, "Fatal Error", self.mediaObject.errorString())
    # else:
    # QMessageBox.warning(self.__main_window, "Error", self.mediaObject.errorString())
    #
    # elif new_state == Phonon.PlayingState:
    # self.playAction.setEnabled(False)
    # self.pauseAction.setEnabled(True)
    # self.stopAction.setEnabled(True)
    #
    #     elif new_state == Phonon.StoppedState:
    #         self.stopAction.setEnabled(False)
    #         self.playAction.setEnabled(True)
    #         self.pauseAction.setEnabled(False)
    #         self.timeLcd.display("00:00")
    #
    #     elif new_state == Phonon.PausedState:
    #         self.pauseAction.setEnabled(False)
    #         self.stopAction.setEnabled(True)
    #         self.playAction.setEnabled(True)

    def play(self):
        self.mediaObject.play()

    def pause(self):
        self.mediaObject.pause()

    def stop(self):
        self.mediaObject.stop()
