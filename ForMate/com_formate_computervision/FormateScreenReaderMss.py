import numpy
from PIL import Image
from PyQt5.QtCore import pyqtSignal, QThread
from PIL import ImageChops  # $ pip install pillow
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QApplication
from pyscreenshot import grab  # $ pip install pyscreenshot
import time
import io
import mss
from com_formate_glass.FormateRect import FormateRect
from datetime import datetime

from com_formate_logs.FormateLogger import FormateLogger


class FormateScreenReaderMss(QThread):

    def __init__(self, glass):
        super().__init__()
        self.render_scheduler = glass.scheduler
        self.desktop_size = QApplication.desktop().geometry()

    def screenshot(self):
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[0]
            im_mss = mss_instance.grab(monitor)
        im_mss_arr = numpy.asarray(im_mss)
        im = Image.fromarray(im_mss_arr)
        return im

    def run(self):
        #print("SCREENSHOT THREAD: QThread running screenreader")
        while True:
            start = time.time()
            im = self.screenshot()
            end = time.time()
            FormateLogger.log("SCREENSHOT THREAD, Time take from FormateScreenshotReader 1, " + str(end - start))
            fp = FormateRect(self.desktop_size.x(), self.desktop_size.y(), self.desktop_size.width(), self.desktop_size.height(), t="screenshot_reader", im=im.convert(mode="L"))
            #print("SCREENSHOT THREAD: Captured changing image crop...")
            self.render_scheduler.append_screenshot(fp)
            #im.show()
            while True:
                start = time.time()
                current_screen = self.screenshot()
                # current_screen.show()
                diff = ImageChops.difference(im, current_screen)
                #diff.show()
                end = time.time()
                FormateLogger.log("SCREENSHOT THREAD, Time take from FormateScreenshotReader 2, " + str(end - start))
                bbox = diff.getbbox()
                self.sleep(3)
                if bbox is not None:  # exact comparison
                    break
            cropped_area = im.crop(bbox).convert(mode="L")
            #cropped_area.show()
            #print("SCREENSHOT THREAD: " + str(bbox))
            fp = FormateRect(bbox[0], bbox[1], bbox[2], bbox[3], t="screenshot_reader", im=cropped_area)
            #print("SCREENSHOT THREAD: Captured changing image crop...")
            self.render_scheduler.append_screenshot(fp)
            #print("SCREENSHOT THREAD: Screenshot added to scheduler for Tesseract processing...")
