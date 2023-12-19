import pyautogui
from PyQt5.QtCore import QThread, pyqtSignal

from com_formate_glass.FormateRect import FormateRect
import time
from datetime import datetime

from com_formate_logs.FormateLogger import FormateLogger


class FormateRenderScheduler(QThread):
    # Renders the elements in the screen in the best order so there is no latency for the user

    render_button_signal = pyqtSignal(FormateRect)

    def __init__(self, glass):
        super().__init__()
        self.render_scheduler = []
        self.screenshots = []

    def append(self, rect):
        self.render_scheduler.append(rect)

    def add(self, many_rects):
        self.render_scheduler = self.render_scheduler + many_rects

    def append_screenshot(self, screenshot):
        self.screenshots.append(screenshot)

    def sort_queue(self, currentMouseX, currentMouseY):
        # Schedule elements to be render closer to the mouse and prioritizing smaller screenshot crops
        self.render_scheduler.sort(key=lambda image_rect: (
                (abs(image_rect.x - currentMouseX) + abs(image_rect.y - currentMouseY)) + (
                (image_rect.x - image_rect.w) * (image_rect.y - image_rect.h))), reverse=False)

    def run(self):
        #print("SCHEDULER THREAD: is running...")
        while True:
            if len(self.render_scheduler) > 0:
                old_hash = hash(str(self.render_scheduler))
                while old_hash != hash(str(self.render_scheduler)):
                    currentMouseX, currentMouseY = pyautogui.position()
                    #print("Current mouse position: " + str(currentMouseX) + "," + str(currentMouseY))
                    start = time.time()
                    self.sort_queue(currentMouseX, currentMouseY)
                    end = time.time()
                    FormateLogger.log("SCHEDULER THREAD, Sort elements from button render queue closer to the mouse, " + str(end - start))
                    #print("SCHEDULER THREAD: Sorting buttons closer to the mouse and by smaller size" + str(self.render_scheduler))
                    old_hash = hash(str(self.render_scheduler))
