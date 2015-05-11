# -*- coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL, QObject, SLOT, pyqtSlot, QRect, QPoint, QSize, Qt
from PyQt4.QtGui import QMainWindow, QPixmap, QApplication, QSizePolicy, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QTableWidget, QFrame, QAbstractItemView, QIcon, QPainter, QBrush, QColor, QFont
from PyQt4.phonon import Phonon
from Core.AudioManager import AudioManager
from Core.Enum import Enum
from Core.MStyleSetter import MStyleSetter
from Widget.MActionBar import MActionBar
from Widget.MButton import MButton
from Widget.MFrame import MFrame
from Widget.MLyricPanel import MLyricPanel
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class ModiaWindow(QMainWindow):
    CursorLocation = Enum(
        ['WINDOW_LEFT', 'WINDOW_RIGHT', 'WINDOW_TOP', 'WINDOW_BOTTOM', 'WINDOW_LEFT_TOP', 'WINDOW_RIGHT_TOP',
         'WINDOW_LEFT_BOTTOM', 'WINDOW_RIGHT_BOTTOM', 'WINDOW_TITLE_BAR', 'SCREEN_LEFT', 'SCREEN_RIGHT', 'SCREEN_TOP'])

    StickType = Enum(['LEFT', 'RIGHT', 'FULL_SCREEN'])

    def __init__(self, parent=None):
        super(ModiaWindow, self).__init__(parent)
        self.__pic_bg = QPixmap(':resource')
        self.WIDTH_MIN = 721
        self.HEIGHT_MIN = 500
        self.WIDTH_DEFAULT = 721
        self.HEIGHT_DEFAULT = 599
        self.WIDTH_BORDER_TOP = 28
        self.WIDTH_BORDER_RIGHT = 12
        self.WIDTH_BORDER_BOTTOM = 14
        self.WIDTH_BORDER_LEFT = 12
        self.OFFSET_BORDER_TOP = 6
        self.OFFSET_BORDER_RIGHT = 8
        self.OFFSET_BORDER_BOTTOM = 10
        self.OFFSET_BORDER_LEFT = 8
        self.WIDTH_FRAME_LEFT = 360
        self.__cursor_loc = None
        self.__is_fixed_size = False
        self.__is_fixed_width = False
        self.__is_fixed_height = False
        self.__is_maximized = False
        self.__is_zdt = False
        self.__is_sticking = False
        self.__is_sticked = False
        self.__lyric_shown = True
        self.__is_suspended = True
        self.__move_point = None
        self.__cursor_changed = False
        self.__mouse_pressed = False
        self.__window_resizing = False
        self.__setup_ui()
        self.__geometry_frame = self.geometry()
        self.__register_actions()
        self.__audio_manager = AudioManager(self, self.lyric_panel)

    def __setup_ui(self):
        self.setWindowTitle(QApplication.applicationName())
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowModality(Qt.WindowModal)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setAnimated(True)
        self.setMinimumSize(self.WIDTH_MIN + self.OFFSET_BORDER_RIGHT + self.OFFSET_BORDER_LEFT,
                            self.HEIGHT_MIN + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
        self.resize(self.WIDTH_DEFAULT + self.OFFSET_BORDER_RIGHT + self.OFFSET_BORDER_LEFT,
                    self.HEIGHT_DEFAULT + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
        self.setWindowIcon(QIcon(':logo'))
        # Title bar initialization start.
        self.__btn_title_close = MButton(self, MButton.Type.Close)
        self.__btn_title_close.setGeometry(14, 11, 12, 13)
        self.__btn_title_close.setToolTip('退出')
        self.__btn_title_maximize = MButton(self, MButton.Type.Maximize)
        self.__btn_title_maximize.setGeometry(self.__btn_title_close.x() + 16, 11, 12, 13)
        self.__btn_title_maximize.setToolTip('最大化')
        self.__btn_title_minimize = MButton(self, MButton.Type.Minimize)
        self.__btn_title_minimize.setGeometry(self.__btn_title_maximize.x() + 16, 11, 12, 13)
        self.__btn_title_minimize.setToolTip('最小化')
        self.frame = MFrame(self)
        horizontal_layout = QHBoxLayout(self.frame)
        horizontal_layout.setContentsMargins(0, 0, 4, 0)
        horizontal_layout.setSpacing(5)
        # Left panel initialization start.
        frame_main_panel = MFrame(self.frame)
        size_policy_v_expand = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        size_policy_v_expand.setHorizontalStretch(0)
        size_policy_v_expand.setVerticalStretch(0)
        size_policy_v_expand.setHeightForWidth(frame_main_panel.sizePolicy().hasHeightForWidth())
        frame_main_panel.setSizePolicy(size_policy_v_expand)
        frame_main_panel.setMinimumSize(self.WIDTH_FRAME_LEFT, 0)
        horizontal_layout.addWidget(frame_main_panel)
        verticalLayout = QVBoxLayout(frame_main_panel)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setSpacing(0)
        self.__action_bar = MActionBar(frame_main_panel)
        size_policy_h_expand = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy_h_expand.setHorizontalStretch(0)
        size_policy_h_expand.setVerticalStretch(0)
        size_policy_h_expand.setHeightForWidth(self.__action_bar.sizePolicy().hasHeightForWidth())
        self.__action_bar.setSizePolicy(size_policy_h_expand)
        self.__action_bar.setMinimumSize(0, 136)
        verticalLayout.addWidget(self.__action_bar)
        frame_music_list = MFrame(frame_main_panel)
        size_policy_all_expand = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy_all_expand.setHorizontalStretch(0)
        size_policy_all_expand.setVerticalStretch(0)
        size_policy_all_expand.setHeightForWidth(frame_music_list.sizePolicy().hasHeightForWidth())
        frame_music_list.setSizePolicy(size_policy_all_expand)
        verticalLayout.addWidget(frame_music_list)
        gridLayout = QGridLayout(frame_music_list)
        gridLayout.setContentsMargins(9, 2, 9, 5)
        self.__music_table = QTableWidget(0, 2, frame_music_list)
        self.__music_table.setFrameShape(QFrame.StyledPanel)
        self.__music_table.setHorizontalHeaderLabels(('标题', '时长'))
        self.__music_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.__music_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.__music_table.horizontalHeader().setVisible(False)
        self.__music_table.verticalHeader().setVisible(False)
        self.__music_table.setColumnWidth(0, 290)
        self.__music_table.setColumnWidth(1, 50)
        MStyleSetter.setStyle(self.__music_table, ':qss_tbl_music_list')
        gridLayout.addWidget(self.__music_table, 0, 0, 1, 1)
        # Lyric panel initialization start.
        self.lyric_panel = MLyricPanel(self.frame)
        size_policy_all_expand.setHeightForWidth(self.lyric_panel.sizePolicy().hasHeightForWidth())
        self.lyric_panel.setSizePolicy(size_policy_all_expand)
        horizontal_layout.addWidget(self.lyric_panel)

    def __register_actions(self):
        QObject.connect(self.__btn_title_close, SIGNAL('clicked()'), self, SLOT('close()'))
        QObject.connect(self.__btn_title_maximize, SIGNAL('clicked()'), self, SLOT('showMaximized()'))
        QObject.connect(self.__btn_title_minimize, SIGNAL('clicked()'), self, SLOT('showMinimized()'))
        QObject.connect(self.__action_bar.get_widget('BTN_PREVIOUS'), SIGNAL('clicked()'), self, SLOT('__previous()'))
        QObject.connect(self.__action_bar.get_widget('BTN_NEXT'), SIGNAL('clicked()'), self, SLOT('__next()'))
        QObject.connect(self.__action_bar.get_widget('BTN_PLAY_PAUSE'), SIGNAL('clicked()'), self,
                        SLOT('__play_pause()'))
        QObject.connect(self.__action_bar.get_widget('BTN_STOP'), SIGNAL('clicked()'), self, SLOT('__stop()'))
        QObject.connect(self.__action_bar.get_widget('BTN_LYRIC'), SIGNAL('clicked()'), self,
                        SLOT('__show_hide_lyric()'))
        QObject.connect(self.__action_bar.get_widget('BTN_ADD_MUSIC'), SIGNAL('clicked()'), self,
                        SLOT('__add_music()'))
        self.__music_table.cellDoubleClicked.connect(self.__cell_double_clicked)

    @pyqtSlot()
    def __previous(self):
        self.__audio_manager.previous()

    @pyqtSlot()
    def __next(self):
        self.__audio_manager.next()

    @pyqtSlot()
    def __play_pause(self):
        if self.__is_suspended:
            self.__audio_manager.play()
        else:
            self.__audio_manager.pause()

    @pyqtSlot()
    def __stop(self):
        self.__audio_manager.stop()

    def __cell_double_clicked(self, row, column):
        self.__stop()
        self.__audio_manager.clearQueue()
        self.__audio_manager.setCurrentSourceByIndex(row)
        if self.__audio_manager.getMediaObjectState() == Phonon.PlayingState:
            self.__audio_manager.stop()
        else:
            self.__audio_manager.play()

    @pyqtSlot()
    def __show_hide_lyric(self):
        if self.__lyric_shown:
            self.__action_bar.get_widget('BTN_LYRIC').setMStyle(MButton.Type.Show_Lyric)
            self.__geometry_frame = self.geometry()
            self.setMinimumSize(360, self.HEIGHT_MIN + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
            self.resize(376, self.height())
            self.__is_fixed_size = True
        else:
            self.__action_bar.get_widget('BTN_LYRIC').setMStyle(MButton.Type.Hide_Lyric)
            self.resize(self.__geometry_frame.width(), self.__geometry_frame.height())
            self.setMinimumSize(self.WIDTH_MIN + self.OFFSET_BORDER_RIGHT + self.OFFSET_BORDER_LEFT,
                                self.HEIGHT_MIN + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
            self.__is_fixed_size = False
        self.__lyric_shown = not self.__lyric_shown

    @pyqtSlot()
    def __add_music(self):
        self.__audio_manager.addMusic()

    def getActionBar(self):
        return self.__action_bar

    def getMusicTable(self):
        return self.__music_table

    def __get_cursor_location(self, event):
        if event.globalX() == 0:
            return self.CursorLocation.SCREEN_LEFT
        if QApplication.desktop().screenGeometry().width() - event.globalX() == 1:
            return self.CursorLocation.SCREEN_RIGHT
        if event.globalY() == 0:
            return self.CursorLocation.SCREEN_TOP
        if event.pos().y() < 27 and event.pos().y() - 2 > self.OFFSET_BORDER_TOP and event.pos().x() + self.OFFSET_BORDER_RIGHT < self.width() and event.pos().x() + 1 > self.OFFSET_BORDER_LEFT:
            return self.CursorLocation.WINDOW_TITLE_BAR
        permissible_var = 2
        if event.pos().x() + permissible_var >= self.OFFSET_BORDER_LEFT and event.pos().x() - permissible_var <= self.OFFSET_BORDER_LEFT:
            if event.pos().y() + self.OFFSET_BORDER_BOTTOM + permissible_var >= self.rect().bottom() and event.pos().y() + self.OFFSET_BORDER_BOTTOM - permissible_var <= self.rect().bottom():
                return self.CursorLocation.WINDOW_LEFT_BOTTOM
            if event.pos().y() + permissible_var >= self.OFFSET_BORDER_TOP and event.pos().y() - permissible_var <= self.OFFSET_BORDER_TOP:
                return self.CursorLocation.WINDOW_LEFT_TOP
            return self.CursorLocation.WINDOW_LEFT
        if event.pos().x() + self.OFFSET_BORDER_RIGHT + permissible_var >= self.rect().right() and event.pos().x() + self.OFFSET_BORDER_RIGHT - permissible_var <= self.rect().right():
            if event.pos().y() + self.OFFSET_BORDER_BOTTOM + permissible_var >= self.rect().bottom() and event.pos().y() + self.OFFSET_BORDER_BOTTOM - permissible_var <= self.rect().bottom():
                return self.CursorLocation.WINDOW_RIGHT_BOTTOM
            if event.pos().y() + permissible_var >= self.OFFSET_BORDER_TOP and event.pos().y() - permissible_var <= self.OFFSET_BORDER_TOP:
                return self.CursorLocation.WINDOW_RIGHT_TOP
            return self.CursorLocation.WINDOW_RIGHT
        if event.pos().y() + permissible_var >= self.OFFSET_BORDER_TOP and event.pos().y() - permissible_var <= self.OFFSET_BORDER_TOP:
            return self.CursorLocation.WINDOW_TOP
        if event.pos().y() + self.OFFSET_BORDER_BOTTOM + permissible_var >= self.rect().bottom() and event.pos().y() + self.OFFSET_BORDER_BOTTOM - permissible_var <= self.rect().bottom():
            return self.CursorLocation.WINDOW_BOTTOM
        return -1

    def __set_cursor_shape(self, flag):
        if self.__is_fixed_size:
            return
        if flag == self.CursorLocation.WINDOW_LEFT or flag == self.CursorLocation.WINDOW_RIGHT:
            if self.__is_fixed_width:
                self.setCursor(Qt.ArrowCursor)
                return False
            self.setCursor(Qt.SizeHorCursor)
            return True
        if flag == self.CursorLocation.WINDOW_TOP or flag == self.CursorLocation.WINDOW_BOTTOM:
            if self.__is_fixed_height:
                self.setCursor(Qt.ArrowCursor)
                return False
            self.setCursor(Qt.SizeVerCursor)
            return True
        if self.__is_fixed_width or self.__is_fixed_height:
            self.setCursor(Qt.ArrowCursor)
            return False
        if flag == self.CursorLocation.WINDOW_LEFT_TOP or flag == self.CursorLocation.WINDOW_RIGHT_BOTTOM:
            self.setCursor(Qt.SizeFDiagCursor)
            return True
        if flag == self.CursorLocation.WINDOW_RIGHT_TOP or flag == self.CursorLocation.WINDOW_LEFT_BOTTOM:
            self.setCursor(Qt.SizeBDiagCursor)
            return True
        self.setCursor(Qt.ArrowCursor)
        return False

    def __change_window_size(self, flag, pos_global):
        pos_global = self.mapToParent(pos_global)
        global_x = pos_global.x() - self.OFFSET_BORDER_LEFT
        global_y = pos_global.y() - self.OFFSET_BORDER_TOP
        widget_x = self.pos().x()
        widget_y = self.pos().y()
        length_l = widget_x + self.width() - global_x
        length_r = global_x - widget_x + 1 + self.OFFSET_BORDER_RIGHT + self.OFFSET_BORDER_LEFT
        length_t = widget_y + self.height() - global_y
        length_b = global_y - widget_y + 1 + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM
        if length_l <= self.WIDTH_MIN:
            global_x = self.pos().x()
        if length_t <= self.HEIGHT_MIN:
            global_y = self.pos().y()
        if flag == self.CursorLocation.WINDOW_LEFT:
            self.setGeometry(global_x, widget_y, length_l, self.height())
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_RIGHT:
            self.setGeometry(widget_x, widget_y, length_r, self.height())
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_TOP:
            self.setGeometry(widget_x, global_y, self.width(), length_t)
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_BOTTOM:
            self.setGeometry(widget_x, widget_y, self.width(), length_b)
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_LEFT_TOP:
            self.setGeometry(global_x, global_y, length_l, length_t)
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_LEFT_BOTTOM:
            self.setGeometry(global_x, widget_y, length_l, length_b)
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_RIGHT_TOP:
            self.setGeometry(widget_x, global_y, length_r, length_t)
            self.__geometry_frame = self.geometry()
            return
        if flag == self.CursorLocation.WINDOW_RIGHT_BOTTOM:
            self.setGeometry(widget_x, widget_y, length_r, length_b)
            self.__geometry_frame = self.geometry()
            return

    def __switch_max_button(self, b_style):
        self.__btn_title_maximize.setMStyle(b_style)
        if b_style == MButton.Type.Maximize:
            self.__btn_title_maximize.setToolTip('最大化')
            return
        if b_style == MButton.Type.Restore:
            self.__btn_title_maximize.setToolTip('向下还原')
            return

    def __window_stick_to(self, s_type):
        if self.__is_sticking:
            return
        if s_type == self.StickType.LEFT:
            geometry_tgt = QRect(-self.OFFSET_BORDER_LEFT, -self.OFFSET_BORDER_TOP,
                                 QApplication.desktop().screenGeometry().width() / 2 + self.OFFSET_BORDER_LEFT + self.OFFSET_BORDER_RIGHT,
                                 QApplication.desktop().availableGeometry().height() + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
            if self.geometry() != geometry_tgt:
                self.setGeometry(geometry_tgt)
                self.__is_sticking = True
                return
        if s_type == self.StickType.RIGHT:
            geometry_tgt = QRect(QApplication.desktop().screenGeometry().width() / 2 - self.OFFSET_BORDER_LEFT,
                                 -self.OFFSET_BORDER_TOP,
                                 QApplication.desktop().screenGeometry().width() / 2 + self.OFFSET_BORDER_LEFT + self.OFFSET_BORDER_RIGHT,
                                 QApplication.desktop().availableGeometry().height() + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
            if self.geometry() != geometry_tgt:
                self.setGeometry(geometry_tgt)
                self.__is_sticking = True
                return
        if s_type == self.StickType.FULL_SCREEN:
            self.setGeometry(- self.OFFSET_BORDER_LEFT, - self.OFFSET_BORDER_TOP,
                             QApplication.desktop().availableGeometry().width() + self.OFFSET_BORDER_RIGHT + self.OFFSET_BORDER_LEFT,
                             QApplication.desktop().availableGeometry().height() + self.OFFSET_BORDER_TOP + self.OFFSET_BORDER_BOTTOM)
            self.__is_sticking = True
            return

    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, 12, self.WIDTH_BORDER_TOP, self.__pic_bg, 0, 0, 12, self.WIDTH_BORDER_TOP)
        painter.drawPixmap(self.WIDTH_BORDER_LEFT, 0, self.width() - self.WIDTH_BORDER_RIGHT - self.WIDTH_BORDER_LEFT,
                           self.WIDTH_BORDER_TOP, self.__pic_bg, 12, 0, 1, self.WIDTH_BORDER_TOP)
        painter.drawPixmap(self.width() - self.WIDTH_BORDER_RIGHT, 0, self.__pic_bg, 13, 0, 12, self.WIDTH_BORDER_TOP)
        painter.drawPixmap(0, self.height() - self.WIDTH_BORDER_BOTTOM, self.__pic_bg, 0, 90, 12, 14)
        painter.drawPixmap(0, self.WIDTH_BORDER_TOP, self.WIDTH_BORDER_LEFT,
                           self.height() - self.WIDTH_BORDER_BOTTOM - self.WIDTH_BORDER_TOP, self.__pic_bg, 0, 89, 12,
                           1)
        painter.drawPixmap(self.width() - self.WIDTH_BORDER_RIGHT, self.WIDTH_BORDER_TOP, self.WIDTH_BORDER_LEFT,
                           self.height() - self.WIDTH_BORDER_BOTTOM - self.WIDTH_BORDER_TOP, self.__pic_bg, 13, 89, 12,
                           1)
        painter.drawPixmap(self.WIDTH_BORDER_LEFT, self.height() - self.WIDTH_BORDER_BOTTOM,
                           self.width() - self.WIDTH_BORDER_RIGHT - self.WIDTH_BORDER_LEFT, self.WIDTH_BORDER_BOTTOM,
                           self.__pic_bg, 12, 90, 1, 14)
        painter.drawPixmap(self.width() - self.WIDTH_BORDER_RIGHT, self.height() - self.WIDTH_BORDER_BOTTOM,
                           self.__pic_bg, 13, 90, 12, 14)
        painter.fillRect(self.WIDTH_BORDER_LEFT - 4, self.WIDTH_BORDER_TOP,
                         self.width() - self.WIDTH_BORDER_LEFT - self.WIDTH_BORDER_RIGHT + 8,
                         self.height() - self.WIDTH_BORDER_BOTTOM - self.WIDTH_BORDER_TOP,
                         QBrush(QColor(255, 255, 255)))
        painter.setFont(QFont('Microsoft Yahei', 8, QFont.Bold))
        painter.setPen(QColor(250, 250, 250, 220))
        painter.drawText(1, 5, self.width(), 27, Qt.AlignHCenter | Qt.AlignVCenter, self.windowTitle())
        painter.setPen(QColor(50, 50, 50, 255))
        painter.drawText(0, 4, self.width(), 27, Qt.AlignHCenter | Qt.AlignVCenter, self.windowTitle())
        painter.setPen(QColor(142, 142, 142, 255))
        if self.width() > 380:
            painter.drawLine(self.WIDTH_FRAME_LEFT + self.OFFSET_BORDER_LEFT, self.OFFSET_BORDER_TOP + 22,
                             self.WIDTH_FRAME_LEFT + self.OFFSET_BORDER_LEFT,
                             self.height() - self.OFFSET_BORDER_BOTTOM - 1)

    @pyqtSlot()
    def showMaximized(self):
        if self.__is_sticked:
            return
        if self.__is_maximized:
            self.setGeometry(self.__geometry_frame)
            self.__switch_max_button(MButton.Type.Maximize)
            self.__is_maximized = False
        else:
            self.__geometry_frame = self.geometry()
            self.__window_stick_to(self.StickType.FULL_SCREEN)
            self.__switch_max_button(MButton.Type.Restore)
            self.__is_maximized = True

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if self.__get_cursor_location(event) == self.CursorLocation.WINDOW_TITLE_BAR:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if self.__get_cursor_location(event) == self.CursorLocation.WINDOW_TITLE_BAR:
            self.__mouse_pressed = True
        if self.__cursor_changed:
            self.__window_resizing = True
        self.__move_point = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.__window_resizing:
            self.__change_window_size(self.__cursor_loc, event.pos())
            return
        else:
            self.__cursor_loc = self.__get_cursor_location(event)
            self.__cursor_changed = self.__set_cursor_shape(self.__cursor_loc)
        if not self.__mouse_pressed:
            return
        if self.__is_maximized and not self.__is_sticked:
            self.resize(self.__geometry_frame.size())
            self.__switch_max_button(MButton.Type.Maximize)
            self.__is_maximized = False
            if event.pos().x() < self.__geometry_frame.width():
                self.__is_zdt = False
            else:
                self.__is_zdt = True
                self.move(event.globalPos() - QPoint(self.width() / 2, 15))
        elif not self.__is_sticking and event.globalPos().y() < QApplication.desktop().availableGeometry().height():
            if not self.__is_zdt:
                self.move(event.globalPos() - self.__move_point)
            else:
                self.move(event.globalPos() - QPoint(self.width() / 2, 15))
        self.__cursor_loc = self.__get_cursor_location(event)
        if self.__cursor_loc == self.CursorLocation.SCREEN_LEFT:
            if self.__lyric_shown:
                self.__window_stick_to(self.StickType.LEFT)
        elif self.__cursor_loc == self.CursorLocation.SCREEN_RIGHT:
            if self.__lyric_shown:
                self.__window_stick_to(self.StickType.RIGHT)
        elif self.__cursor_loc == self.CursorLocation.SCREEN_TOP:
            if self.__lyric_shown:
                self.showMaximized()
            self.__is_sticked = True
        else:
            if self.width() - self.OFFSET_BORDER_LEFT - self.OFFSET_BORDER_RIGHT >= QApplication.desktop().screenGeometry().width():
                self.resize(800, self.height())
            if self.height() - self.OFFSET_BORDER_TOP - self.OFFSET_BORDER_BOTTOM >= QApplication.desktop().availableGeometry().height():
                self.resize(self.width(), 600)
            self.__is_sticking = False
            self.__is_sticked = False

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if self.geometry().y() < -self.OFFSET_BORDER_TOP:
            self.setGeometry(self.geometry().x(), - self.OFFSET_BORDER_TOP, self.geometry().width(),
                             self.geometry().height())
        self.__mouse_pressed = False
        self.__window_resizing = False
        self.__is_sticking = False
        self.__is_sticked = False
        if not self.__is_maximized:
            self.__is_zdt = False

    def resizeEvent(self, event):
        self.frame.setGeometry(self.OFFSET_BORDER_LEFT, self.OFFSET_BORDER_TOP + 22,
                               self.width() - self.OFFSET_BORDER_LEFT - self.OFFSET_BORDER_RIGHT,
                               self.height() - self.OFFSET_BORDER_TOP - self.OFFSET_BORDER_BOTTOM - 26)

    def setFixedSize(self, *__args):
        count_parm = len(__args)
        if count_parm == 0 or count_parm > 2:
            raise TypeError('Argument error occurred. (1 or 2 given)')
        if count_parm == 1:
            if isinstance(__args[0], QSize):
                super(ModiaWindow, self).setFixedSize(__args[0])
                self.__is_fixed_size = True
            else:
                raise ValueError('Given argument not QSize type. (QSize type required for 1 argument)')
        else:
            if isinstance(__args[0], int) and isinstance(__args[1], int):
                super(ModiaWindow, self).setFixedSize(__args[0], __args[1])
                self.__is_fixed_size = True
            else:
                raise ValueError('Given arguments not int type. (int type required for 2 arguments)')

    def setFixedWidth(self, p_int):
        if not isinstance(p_int, int):
            raise ValueError('Given argument not int type. (int type required)')
        self.resize(p_int, self.height())
        self.__is_fixed_width = True

    def setFixedHeight(self, p_int):
        if not isinstance(p_int, int):
            raise ValueError('Given argument not int type. (int type required)')
        self.resize(self.width(), p_int)
        self.__is_fixed_height = True

    def setSuspendStatus(self, bool_suspended):
        self.__is_suspended = bool_suspended
