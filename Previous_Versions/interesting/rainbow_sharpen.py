filter = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])

    height, width = frame.shape[:2]
    # y = np.ones((height, width), np.uint8) * 128

    #
    # frame2 =  cv2.GaussianBlur(frame, (0, 0), cv2.BORDER_DEFAULT)
    # frame = cv2.addWeighted(frame, 1.5, frame2, -0.5, 0, frame2)
    frame = cv2.filter2D(frame, -1, filter)

    filter = np.array([
        [1, 1, 1],
        [1, 5, 1],
        [1, 1, 1]
    ])
    frame = cv2.filter2D(frame, -1, filter)

    return frame