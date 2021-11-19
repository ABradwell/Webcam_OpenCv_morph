
from threading import Thread
import cv2
from time import sleep
import numpy as np

"""
    The class VideoGetter, and general multithread approach was found on https://nrsyed.com/2018/07/05/multithreading-with-opencv-python-to-improve-video-processing-performance/
"""
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
        while (not self.stopped):
            cv2.waitKey(10)
            # print("\t===GET!")

            if not self.grabbed:
                self.stop()
            else:
                
                (self.grabbed, cur_frame) = self.camera.read()
                self.frame_queue.append(cur_frame)
                # print("\t\t===Got Frame {}".format(len(self.frame_queue)))
                
    def stop(self):
        self.stopped = True


class VideoShower:
    """
    
    """

    def __init__(self, frame_queue, fps):
        self.frame_queue = frame_queue
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):

        while (not self.stopped):
            # print("\t---SHOW!")
            cv2.waitKey(10)

            if len(self.frame_queue) > 0:
                cur_frame = self.frame_queue.pop()

                cur_frame = modify(cur_frame)

                # print("\t\t---Popped Frame {}".format(len(self.frame_queue)))
                cv2.imshow("Output", cur_frame)

            # else:
                # print("Empty Frame")

    def stop(self):
        self.stopped = True


def nothing(x):
    pass

def dothreshold(frame):
    # if len(frame) == 3:
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # else:
    #     grey_frame = frame

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
    # y = np.ones((height, width), np.uint8) * 128
    # grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.add(cv2.filter2D(grey_frame, -1, filter), y) # emboss on bottom left side
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
    # frame =  cv2.GaussianBlur(frame, (0, 0), cv2.BORDER_DEFAULT)
    return cv2.GaussianBlur(frame, (0, 0), cv2.BORDER_DEFAULT)

def lighten(frame):
    return frame

def darken(frame):
    return frame

def get_bool_list():
    threshold_bool = cv2.getTrackbarPos("threshold",'filterFrame')
    sharpen_bool = cv2.getTrackbarPos("sharpen",'filterFrame')
    emboss_bool = cv2.getTrackbarPos("emboss",'filterFrame')
    edge_detection_bool = cv2.getTrackbarPos("edge_detection",'filterFrame')
    dither_bool = cv2.getTrackbarPos("dither",'filterFrame')
    blur_bool = cv2.getTrackbarPos("blur",'filterFrame')
    lighten_bool = cv2.getTrackbarPos("lighten",'filterFrame')
    darken_bool = cv2.getTrackbarPos("darken",'filterFrame')

    bool_list = [    
        threshold_bool,
        sharpen_bool,
        emboss_bool,
        edge_detection_bool,
        dither_bool,
        blur_bool,
        lighten_bool, 
        darken_bool,
    ]

    return bool_list

def modify(frame):
    
    # bool_list dictionary...
    #
    #   1:    Threshold 
    #   2:    Sharpen
    #   3:    Emboss
    #   4:    Edge Detection
    #   5:    Dither
    #   6:    Blur
    #   7:    Lighten
    #   8:    Darken
    bool_list = get_bool_list()
    
    if bool_list[1]:
        frame = sharpen(frame)
    if bool_list[2]:
        frame = emboss(frame)
    if bool_list[3]:
        frame = edge_detection(frame)
    if bool_list[4]:
        frame = dither(frame)
    if bool_list[5]:
        frame = blur(frame)
    if bool_list[6]:
        frame = lighten(frame)
    if bool_list[7]:
        frame = darken(frame)
    if bool_list[0]:
        frame = dothreshold(frame)

    return frame






if __name__ == "__main__":
        
    # Step One: Initialize Reading & displaying stream
    # Step Two: Launch both
    # Step Three: 
    # Step Four: 
    # Step Five: 

    print("Main called")
    cv2.namedWindow('filterFrame')

    # create switch for ON/OFF functionality
    cv2.createTrackbar("threshold", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("sharpen", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("emboss", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("edge_detection", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("dither", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("blur", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("lighten", 'filterFrame',0,1,nothing)
    cv2.createTrackbar("darken", 'filterFrame',0,1,nothing)
    
    camera = cv2.VideoCapture(0)
    fps = camera.get(cv2.CAP_PROP_FPS)
    print("Camera Created.")

    video_getter = VideoGetter(camera).start()
    print("Video Getter Created.")

    video_shower = VideoShower(video_getter.frame_queue, fps).start()
    print("Video Shower Created.")

    try: 
        while True:
            if (cv2.waitKey(25) == ord('q') or video_getter.stopped):
                video_getter.stop()
                video_shower.stop()
                break

    except Exception as e:
        video_getter.stop()
        video_shower.stop()

