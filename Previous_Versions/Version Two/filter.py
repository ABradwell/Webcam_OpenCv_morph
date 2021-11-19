import cv2
import numpy as np
from PIL import Image, ImageTk


class VideoFilter:

    def __init__(self, label):
        self.filter_queue = []
        self.out_str = ""
        self.label = label
    
    def add_filter(self, filter_func):

        print("Add filter.")

        self.filter_queue.append(filter_func)
        self.label = self.__str__()
        print(self)

    def remove_filter(self, filter_func):

        print("Remove filter.")
        
        for i in range(len(self.filter_queue)-1, 0, -1):
            if self.filter_queue[i].__name__ == filter_func.__name__:
                del self.filter_queue[i]
                self.label = self.__str__()
                print(self)
                return
        
        print("No such filter is currently in the filter stack.")

    def remove_filters(self, filter_func):

        print("Remove filters.")

        if filter_func in self.filter_queue:
            self.filter_queue.remove(filter_func)
            self.label = self.__str__()
            print(self)
            return

        print("No such filter is currently in the filter stack.")
            
    def filter(self, frame):

        for func in self.filter_queue:
            frame = func(frame)

        self.label = self.__str__()

        return frame
        
    def clear(self):

        print("Clear.")
        
        self.filter_queue = []
        self.label = self.__str__()
        print(self)
    
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
    # y = np.ones((height, width), np.uint8) * 128

    # 
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

def dither(frame):
    return frame


def blur(frame):

    blur_type = "normal"
    kernal = (5, 5)

    if blur_type == "normal":
        return cv2.blur(frame, kernal)
    else:
        return cv2.GaussianBlur(frame, kernal, cv2.BORDER_DEFAULT)


def lighten(frame):
    return frame

def darken(frame):
    return frame
