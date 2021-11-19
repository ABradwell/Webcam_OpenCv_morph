import cv2
import numpy as np
from PIL import Image, ImageTk
import dlib


class VideoFilter:

    def __init__(self, label):
        self.filter_queue = []
        self.out_str = ""
        self.label = label
        self.clear_flag = False
    
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

    def filter(self, frame):

        for func in self.filter_queue:
            frame = func(frame)

        self.label = self.__str__()

        return frame
        
    def clear(self):

        print("Clear.")
        
        self.filter_queue = []
        self.clear_flag = True
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


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def eye_spots(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        gray = frame
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = [landmarks.part(36), landmarks.part(37), landmarks.part(38), landmarks.part(39), landmarks.part(40),
                    landmarks.part(41)]
        right_eye = [landmarks.part(42), landmarks.part(43), landmarks.part(44), landmarks.part(45), landmarks.part(46),
                     landmarks.part(47)]

        min_left_eye_x = min([part.x for part in left_eye])
        max_left_eye_x = max([part.x for part in left_eye])
        min_left_eye_y = min([part.y for part in left_eye])
        max_left_eye_y = max([part.y for part in left_eye])

        cv2.circle(frame, center=(min_left_eye_x, min_left_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(min_left_eye_x, max_left_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(max_left_eye_x, min_left_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(max_left_eye_x, max_left_eye_y), radius=5, color=(0, 255, 0), thickness=-1)

        min_right_eye_x = min([part.x for part in right_eye])
        max_right_eye_x = max([part.x for part in right_eye])
        min_right_eye_y = min([part.y for part in right_eye])
        max_right_eye_y = max([part.y for part in right_eye])

        cv2.circle(frame, center=(min_right_eye_x, min_right_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(min_right_eye_x, max_right_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(max_right_eye_x, min_right_eye_y), radius=5, color=(0, 255, 0), thickness=-1)
        cv2.circle(frame, center=(max_right_eye_x, max_right_eye_y), radius=5, color=(0, 255, 0), thickness=-1)

        break

    return frame
