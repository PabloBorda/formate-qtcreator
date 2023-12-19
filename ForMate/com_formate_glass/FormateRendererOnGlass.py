import time
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal

from com_formate_glass.FormateRect import FormateRect
import pytesseract
import pprint

from com_formate_logs.FormateLogger import FormateLogger


class FormateRendererOnGlass(QThread):
    render_button_signal = pyqtSignal(FormateRect)

    def __init__(self, glass):
        super().__init__()
        self.render_scheduler = glass.scheduler


    def get_text_at_position(self, roi):
        start = time.time()
        text = pytesseract.image_to_string(roi, config='-l eng --oem 1 --psm 7')
        end = time.time()
        FormateLogger.log("RENDER THREAD, Decode text from rect " + FormateLogger.normalize_text(text) + "," + str(end - start))
        return text

    def run(self):
        FormateLogger.log("RENDER THREAD, is running , 0")
        while True:
            while len(self.render_scheduler.render_scheduler) > 0:
                button_rect = self.render_scheduler.render_scheduler.pop(0)
                #print("RENDER THREAD: Pop button_rect from render scheduler to analize text in image")
                button_rect.text = self.get_text_at_position(button_rect.im)
                pprint.pprint(self.render_button_signal.emit(button_rect))
