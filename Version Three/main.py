from threading import Thread
import cv2
from video_players import *
from tkinter import *
from filter import *

import numpy as np


def add_single_filter_button(window, cmd, title, row, col):
    command = lambda: video_filter.add_filter(cmd)
    button = Button(window, text="[{}]".format(title), command=command)
    button.grid(row=row, column=col, sticky=E, pady=3)


def add_single_misc_button(window, cmd, title, row, col):
    button = Button(window, text="[{}]".format(title), command=cmd)
    button.grid(row=row, column=col, sticky=E, pady=3)


def add_button_info(window, cmd, title, row):

    add_command = lambda: video_filter.add_filter(cmd)
    remove_command = lambda: video_filter.remove_filter(cmd)

    add_button = Button(window, text="+{}".format(title), command=add_command)
    remove_button = Button(window, text="-{}".format(title), command=remove_command)

    add_button.grid(row=row, column=1, sticky=E, pady=3, padx=5)
    remove_button.grid(row=row, column=2, sticky=E, pady=3, padx=5)


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
    add_button_info(top, remove_pure, "Remove Pure", 10)

    video_filter = VideoFilter(l)
    add_single_misc_button(top, video_filter.clear, "Clear", 12, 1)
    add_single_filter_button(top, bgr, "BGR", 11, 2)
    add_single_filter_button(top, black_and_white, "B&W", 11, 1)

    camera = cv2.VideoCapture(0)

    video_getter = VideoGetter(camera).start()
    video_shower = VideoShower(video_getter.frame_queue, video_filter, top).start()
    top.mainloop()

    cv2.destroyAllWindows()
