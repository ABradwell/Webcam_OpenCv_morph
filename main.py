"""
    Author: Aiden Stevenson Bradwell
    Date: 2021-11-19
    Affiliation: University of Ottawa, Ottawa, Ontario (Student)

    Description:
        Create two objects, one records frames, one filters the frames and displays them.
        Launch both in parallel processing approach
        User is able to add or remove filters using an OpenCv button bank

    Libraries required:
        opencv-python
        tkinter
        numpy
"""



from threading import Thread
import cv2
from video_players import *
from tkinter import *
from filter import *

import numpy as np


def add_single_filter_button(window, cmd, title, row, col):
    """
        Use for filters which only have one button (IE black & white for example).

        Method designed to reduce repetitive code during initialization.
        Creates a button for a given method.

        :param window: string name of opencv window to be added to
        :param cmd: Command to be called when button pressed
        :param title: string to be shown on button
        :param row: location of button Y
        :param col: location of button X
        :return: None
    """

    command = lambda: video_filter.add_filter(cmd)
    button = Button(window, text="[{}]".format(title), command=command)
    button.grid(row=row, column=col, sticky=E, pady=3)


def add_single_misc_button(window, cmd, title, row, col):
    """
           Use for buttons which do not add a filter (such as clear).
           Creates a button for a given method.

           :param window: string name of opencv window to be added to
           :param cmd: Command to be called when button pressed
           :param title: string to be shown on button
           :param row: location of button Y
           :param col: location of button X
           :return: None
       """

    button = Button(window, text="[{}]".format(title), command=cmd)
    button.grid(row=row, column=col, sticky=E, pady=3)


def add_button_info(window, cmd, title, row):
    """
        Use for buttons which add or remove filters (blur for example).

        Method designed to reduce repetitive code during initialization.
        Creates 3 button for a given filter (add, remove, remove all).

        :param window: string name of opencv window to be added to
        :param cmd: Command to be called when button pressed
        :param title: string to be shown on button
        :param row: row for the three buttons to be placed
        :return: None
    """

    add_command = lambda: video_filter.add_filter(cmd)
    remove_command = lambda: video_filter.remove_filter(cmd)

    add_button = Button(window, text="+{}".format(title), command=add_command)
    remove_button = Button(window, text="-{}".format(title), command=remove_command)

    add_button.grid(row=row, column=1, sticky=E, pady=3, padx=5)
    remove_button.grid(row=row, column=2, sticky=E, pady=3, padx=5)


if __name__ == "__main__":

    # Initialization Steps
    top = Tk()

    l = Label(top, text="").grid(row=0, column=0, columnspan=15)

    # Add all currently supported filtering methods
    add_button_info(top, dothreshold, "Threshold", 2)
    add_button_info(top, sharpen, "Sharpen", 3)
    add_button_info(top, emboss, "Emboss", 4)
    add_button_info(top, edge_detection, "Edge Detection", 5)
    add_button_info(top, dither, "Dither", 6)
    add_button_info(top, blur, "Blur", 7)
    add_button_info(top, lighten, "Lighten", 8)
    add_button_info(top, darken, "Darken", 9)
    add_button_info(top, remove_pure, "Remove Pure", 10)

    # Create filtering object, which stores the requested filters.
    video_filter = VideoFilter(l)
    add_single_misc_button(top, video_filter.clear, "Clear", 12, 1)
    add_single_filter_button(top, bgr, "BGR", 11, 2)
    add_single_filter_button(top, black_and_white, "B&W", 11, 1)

    # Initialize webcam
    camera = cv2.VideoCapture(0)

    # Create webcam object, which adds all frames to the filter's frame-queue
    video_getter = VideoGetter(camera).start()
    video_shower = VideoShower(video_getter.frame_queue, video_filter, top).start()
    top.mainloop()

    # If reached, program has been ended. Destroy all windows.
    cv2.destroyAllWindows()
