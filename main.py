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

    return row + 1


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

    return row + 1

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

    return row+1


def add_blur_buttons(window, row):
    v = IntVar(value=1)
    Label(window, text="Blur Kernel:").grid(row=row, column=0)
    Radiobutton(window, text="1", padx=0, variable=v, command=lambda: video_filter.set_blur_kernel(1)).grid(row=row, column=1)
    Radiobutton(window, text="3", padx=0, variable=v, command=lambda: video_filter.set_blur_kernel(3)).grid(row=row+1, column=1)
    Radiobutton(window, text="5", padx=0, variable=v, command=lambda: video_filter.set_blur_kernel(5)).grid(row=row+2, column=1)
    Radiobutton(window, text="7", padx=0, variable=v, command=lambda: video_filter.set_blur_kernel(7)).grid(row=row+3, column=1)

    Radiobutton(window, text="Normal", padx=0, variable=v, command=lambda: video_filter.set_blur_mode("normal")).grid(row=row + 1, column=2)
    Radiobutton(window, text="Median", padx=0, variable=v, command=lambda: video_filter.set_blur_mode("median")).grid(row=row + 2, column=2)
    Radiobutton(window, text="Gaussian", padx=0, variable=v, command=lambda: video_filter.set_blur_mode("gaussian")).grid(row=row + 3, column=2)

    return row+4


if __name__ == "__main__":

    # Initialization Steps
    top = Tk()

    l = Label(top, text="").grid(row=0, column=0, columnspan=15)
    video_filter = VideoFilter(l)
    # Add all currently supported filtering methods
    row = 0
    row = add_button_info(top, dothreshold, "Threshold", row)
    row = add_button_info(top, sharpen, "Sharpen", row)
    row = add_button_info(top, emboss, "Emboss", row)
    row = add_button_info(top, edge_detection, "Edge Detection", row)
    row = add_button_info(top, blur, "Blur", row)
    row = add_blur_buttons(top, row)
    row = add_button_info(top, lighten, "Lighten", row)
    row = add_button_info(top, darken, "Darken", row)
    row = add_button_info(top, remove_pure, "Remove Pure", row)

    # Create filtering object, which stores the requested filters.

    row = add_single_misc_button(top, video_filter.clear, "Clear", row, 1)
    row = add_single_filter_button(top, bgr, "BGR", row, 2)
    row = add_single_filter_button(top, black_and_white, "B&W", row, 1)

    # Initialize webcam
    camera = cv2.VideoCapture(0)

    # Create webcam object, which adds all frames to the filter's frame-queue
    video_getter = VideoGetter(camera).start()
    video_shower = VideoShower(video_getter.frame_queue, video_filter, top).start()
    top.mainloop()

    # If reached, program has been ended. Destroy all windows.
    cv2.destroyAllWindows()
