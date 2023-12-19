#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

from com_formate_computervision.FormateRenderScheduler import FormateRenderScheduler
from com_formate_computervision.FormateScreenReaderMss import FormateScreenReaderMss

from com_formate_computervision.FormateTesseract import FormateTesseract
from com_formate_glass.FormateButton import FormateButton
from com_formate_glass.FormateRect import FormateRect
from com_formate_glass.FormateRendererOnGlass import FormateRendererOnGlass
from datetime import datetime
from com_formate_logs.FormateLogger import FormateLogger

class FormateTransparentGlass(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window

        allScreens = QApplication.desktop().geometry()

        self.setGeometry(allScreens)
        print("MAIN THREAD: Screen Size is: " + str(allScreens))

        # set the title
        self.buttons = []

        # Implement transparency

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Initialize button render scheduler for faster response time

        self.scheduler = FormateRenderScheduler(self)
        self.scheduler.start()

        # Initialize screen reader that takes screenshots only in screen pixels changing areas

        self.input = FormateScreenReaderMss(self)
        self.input.start()

        # Initialize computer vision thread

        self.vision = FormateTesseract(self)
        self.vision.start()

        # Renders buttons on the glass

        self.button_renderer = FormateRendererOnGlass(self)
        self.button_renderer.render_button_signal.connect(self.render_button)
        self.button_renderer.start()

        # Input transparency for transparent window has a QT bug that turns the window to white instead of transparent
        # we will research this later and even contact QT support people

        # self.setWindowFlags(QtCore.Qt.WindowTransparentForInput)

        # Show the transparent glass

        self.show()

    # Slot to be called when a button has to be displayed

    @QtCore.pyqtSlot(FormateRect)
    def render_button(self, single_rect):
        FormateLogger.log("MAIN THREAD, Rendering button [" + FormateLogger.normalize_text(single_rect.text) + "[" + str(single_rect.x) + "_" +  str(single_rect.y) + "_" + str(single_rect.w) + "_" + str(single_rect.h) + "]],0")
        FormateButton(single_rect, parent=self)

    def paintEvent(self, event):
        FormateLogger.log("MAIN THREAD,refresh,0")

    def settings_dialog(self):
        FormateLogger.log("MAIN THREAD,Settings clicked,0")
