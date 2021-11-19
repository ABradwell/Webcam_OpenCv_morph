from threading import Thread
import cv2
from tkinter.ttk import Label
from tkinter import *
from filter import *

class VideoGetter:
    """

    """

    def __init__(self, src):
        self.camera = src
        (self.grabbed, self.frame) = self.camera.read()
        self.stopped = False
        self.frame_queue = []

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:

            if not self.grabbed:
                self.stop()
            else:

                (self.grabbed, cur_frame) = self.camera.read()
                self.frame_queue.append(cur_frame)

    def stop(self):
        self.stopped = True


class VideoShower:
    """

    """

    def __init__(self, frame_queue, video_filter, gui_frame):
        self.frame_queue = frame_queue
        self.video_filter = video_filter
        self.gui = gui_frame
        self.stopped = False
        self.cur_image = None
        self.panel = None

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):

        while not self.stopped:

            cv2.waitKey(10)

            # if the panel is not None, we need to initialize it
            if len(self.frame_queue) > 0:

                image = self.frame_queue.pop()
                image = self.video_filter.filter(image)

                cv2.imshow("Video Feed...", image)

    def stop(self):
        self.stopped = True
