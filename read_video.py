from time import sleep

import cv2
import numpy as np

i = 0

THRESHOLD = 30


class VideoFrameIsEmpty(Exception):
    pass


def load_video(path: str) -> cv2.VideoCapture:
    "load video to OpenCV"
    def get_frame_length(video: cv2.VideoCapture) -> float:
        "get number of frame in video"
        return video.get(cv2.CAP_PROP_FRAME_COUNT)

    video = cv2.VideoCapture(path)
    video.open(1 + cv2.CAP_DSHOW)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video.set(cv2.CAP_PROP_FOURCC, fourcc)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    video.set(cv2.CAP_PROP_FPS, 60)

    if get_frame_length(video) == 0:
        raise VideoFrameIsEmpty
    else:
        return video


def binarize(image: np.ndarray) -> np.ndarray:
    "convert image to binarized one"
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def diff_image(im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
    "measure difference between 2 images"
    return cv2.absdiff(im1, im2)


def read_frame(video: cv2.VideoCapture):
    "read a frame from video object"
    load_status, data = video.read()
    if load_status:
        return data
    else:
        raise VideoFrameIsEmpty(
            'current frame is perhaps at end of video.')


def show_images(image: np.ndarray, window_name: str) -> None:
    "open window and show image"
    cv2.imshow(window_name, image)


def main():
    PATH = './contextA.avi'
    video = load_video(PATH)

    bg_data = binarize(read_frame(video))
    idx = -1
    while video.isOpened():
        idx += 1
        print(idx)
        r = read_frame(video)
        current_data = binarize(r)
        # 差分の絶対値
        mask = diff_image(current_data, bg_data)
        mask[mask < THRESHOLD] = 0
        mask[mask >= THRESHOLD] = 255
        # show_images(mask, "masked image")
        show_images(r, "current")
        # 背景画像の更新(if idx % 30:)
        bg_data = binarize(read_frame(video))
        sleep(0.1)

    video.release()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
