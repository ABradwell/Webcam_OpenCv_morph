from threading import Thread
import cv2
from video_players import *
from tkinter import *
from filter import *

import numpy as np

"""
    The class VideoGetter, and general multithread approach was found on https://nrsyed.com/2018/07/05/multithreading-with-opencv-python-to-improve-video-processing-performance/
"""


def add_button_info(window, cmd, title, row):
    add_command = lambda: video_filter.add_filter(cmd)
    remove_command = lambda: video_filter.remove_filter(cmd)
    remove_all_command = lambda: video_filter.remove_filters(cmd)

    add_button = Button(window, text="+{}".format(title), command=add_command)
    remove_button = Button(window, text="-{}".format(title), command=remove_command)
    remove_all_button = Button(window, text="--{}".format(title), command=remove_all_command)

    add_button.grid(row=row, column=1, sticky=E, pady=3)
    remove_button.grid(row=row, column=2, sticky=E, pady=3)
    remove_all_button.grid(row=row, column=3, sticky=E, pady=3)


if __name__ == "__main__":
    # create switch for ON/OFF functionality
    top = Tk()
    l = Label(top, text="").grid(row=0, column=0, columnspan=15)
    add_button_info(top, dothreshold, "Threshold", 2)
    add_button_info(top, sharpen, "Sharpen", 3)
    add_button_info(top, emboss, "Emboss", 4)
    add_button_info(top, edge_detection, "Edge Detection", 5)
    add_button_info(top, dither, "Dither", 6)
    add_button_info(top, blur, "Blur", 7)
    add_button_info(top, lighten, "Lighten", 8)
    add_button_info(top, darken, "Darken", 9)

    video_filter = VideoFilter(l)

    camera = cv2.VideoCapture(0)

    # w = Canvas(top, width=1000, height=1000, bd=10, bg='white')
    # w.grid(row=9, column=0, columnspan=15)

    video_getter = VideoGetter(camera).start()
    video_shower = VideoShower(video_getter.frame_queue, video_filter, top).start()
    top.mainloop()

    cv2.destroyAllWindows()
