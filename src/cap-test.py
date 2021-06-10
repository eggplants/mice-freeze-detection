import cv2
import numpy as np


def get_camid_list() -> list[cv2.VideoCapture]:
    """Get a list of ids of camera device."""
    from itertools import count
    ids = []
    for i in count():
        cap: cv2.VideoCapture = cv2.VideoCapture(i)
        if cap.read()[0]:
            ids.append(i)
        else:
            break
        cap.release()
    return ids


def check_camera_connection() -> None:
    """Check the connection between any camera and the PC."""
    import datetime

    print('[', datetime.datetime.now(), ']', 'searching any camera...')
    true_camera_is = []
    for camera_number in range(0, 10):
        cap = cv2.VideoCapture(camera_number)
        ret, frame = cap.read()

        if ret is True:
            true_camera_is.append(camera_number)
            print("camera_number", camera_number, "Find!")

        else:
            print("camera_number", camera_number, "None")
    print("detected: ", len(true_camera_is), "cam(s)")


def main() -> None:
    """Record with VideoCapture"""
    capture: cv2.VideoCapture = cv2.VideoCapture(0)

    while True:
        ret: bool
        frame: np.ndarray
        ret, frame = capture.read()
        # resize the window
        cv2.imshow('title', frame)


if __name__ == '__main__':
    try:
        # main()
        # check_camera_connection()
        lis = get_camid_list()
        print(lis)
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        exit(1)
