"""
    Author: Aiden Stevenson Bradwell
    Date: 2021-11-19
    Affiliation: University of Ottawa, Ottawa, Ontario (Student)

    Description:
        Contains all filters currently supported.
        VideoFilter adds or removes filters, and is a helper class to the VideoShower class
        Works as the active stack of requested filters.

    Libraries required:
        opencv-python
        numpy
"""

import cv2
import numpy as np


class VideoFilter:
    """Implementation of a queue class, which stores filters, and applies them to requested frames"""

    def __init__(self, label):
        self.filter_queue = []
        self.out_str = ""
        self.label = label
        self.blur_kernel = (3, 3)
        self.blur_mode = "normal"
    
    def add_filter(self, filter_func):
        """
        Add a given filter method to the queue

        :param filter_func: filter method to be added to the queue
        :return: None
        """

        print("Add filter.")

        self.filter_queue.append(filter_func)
        self.label = self.__str__()
        print(self)

    def remove_filter(self, filter_func):
        """
        Search the queue from last-to-first, to remove the last instance of
        this function in the queue.

        :param filter_func: Function to be removed
        :return: None
        """

        print("Remove filter.")

        for i in range(len(self.filter_queue)-1, -1, -1):
            if self.filter_queue[i].__name__ == filter_func.__name__:
                del self.filter_queue[i]
                self.label = self.__str__()
                print(self)
                return
        
        print("No such filter is currently in the filter stack.")

    def filter(self, frame):
        """
        Apply all filters in the queue to the given frame

        :param frame: numpy webcam-frame to be filtered
        :return: Filtered frame
        """

        for func in self.filter_queue:
            if func == blur:
                frame = func(frame, self.blur_kernel, self.blur_mode)
            else:
                frame = func(frame)

        self.label = self.__str__()

        return frame
        
    def clear(self):
        """ Remove all filters in the current queue """

        print("Clear.")
        
        self.filter_queue = []
        self.label = self.__str__()
        print(self)

    def set_blur_kernel(self, new_kernel):
        self.blur_kernel = (new_kernel, new_kernel)

    def set_blur_mode(self, blur_mode):

        if blur_mode == "normal":
            self.blur_mode = "normal"

        elif blur_mode == "median":
            self.blur_mode = "median"

        else:
            self.blur_mode = "gaussian"

        print("Blur mode is set to: {}".format(self.blur_mode))

    def __str__(self):
        
        out_string = ""
        for filter in self.filter_queue:
            out_string = "{} -> {}".format(out_string, filter.__name__)

        return out_string


def dothreshold(frame):
    try:
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        grey_frame = frame

    running_threshlimit = 24
    ret, binary_difference = cv2.threshold(grey_frame, running_threshlimit, 255, cv2.THRESH_BINARY)
    return binary_difference


def sharpen(frame):

    filter = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])

    height, width = frame.shape[:2]

    frame2 =  cv2.GaussianBlur(frame, (0, 0), cv2.BORDER_DEFAULT)
    frame = cv2.addWeighted(frame, 1.5, frame2, -0.5, 0, frame2)
    frame = cv2.filter2D(frame, -1, filter)

    return frame


def emboss(frame):

    filter = np.array([
        [1, 1, 0],
        [1, 0, -1],
        [0, -1, -1]
    ])

    height, width = frame.shape[:2]

    frame = cv2.filter2D(frame, -1, filter)

    return frame


def edge_detection(frame):

    lowrange = 100
    highrange = 200

    frame = cv2.Canny(frame, lowrange, highrange)

    return frame


def blur(frame, kernal, blur_mode):

    if blur_mode == "normal":
        return cv2.blur(frame, kernal)
    elif blur_mode == "median":
        return cv2.medianBlur(frame, kernal[0])
    else:
        return cv2.GaussianBlur(frame, kernal, cv2.BORDER_DEFAULT)


def lighten(frame):
    """
    https://www.geeksforgeeks.org/changing-the-contrast-and-brightness-of-an-image-using-python-opencv/
    """

    return brightness_adjustments(frame, 265)


def darken(frame):
    """
    https://www.geeksforgeeks.org/changing-the-contrast-and-brightness-of-an-image-using-python-opencv/
    """

    return brightness_adjustments(frame, 245)


def brightness_adjustments(frame, brightness):
    """ https://www.geeksforgeeks.org/changing-the-contrast-and-brightness-of-an-image-using-python-opencv/ """
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255

        else:
            shadow = 0
            max = 255 + brightness

        al_pha = (max - shadow) / 255
        ga_mma = shadow

        # The function addWeighted calculates
        # the weighted sum of two arrays
        cal = cv2.addWeighted(frame, al_pha,
                              frame, 0, ga_mma)
    else:
        cal = frame

    return cal


def remove_pure(frame):

    try:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        frame = frame

    filter = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])

    frame2 = cv2.GaussianBlur(frame, (0, 0), cv2.BORDER_DEFAULT)
    frame = cv2.addWeighted(frame, 1.5, frame2, -0.5, 0, frame2)
    frame = cv2.filter2D(frame, -1, filter)

    try:
        cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    except:
        frame = frame

    return frame


def black_and_white(frame):
    try:
        greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            greyscale = frame

    return greyscale


def bgr(frame):
    try:
        bgr_scale = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    except:
        bgr_scale = frame

    return bgr_scale