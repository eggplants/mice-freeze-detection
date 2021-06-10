import os
from typing import Any

import cv2
import numpy as np
from cv2 import bgsegm_BackgroundSubtractorMOG as MOG

from DetectedWidget import DetectedWidget


class VideoFrameIsEmpty(Exception):
    pass


class DetectFreezing:
    """Detect moving and freezing behavior from an avi video file."""

    def __init__(self, video_path: str) -> None:
        """Initializer"""
        self.video_path = video_path
        self.video = self.__load_video(video_path)
        self.__wait_sec = int(1000 / self.video.get(cv2.CAP_PROP_FPS))
        self.__video_len = self.__get_frame_length(self.video)

    @staticmethod
    def __load_video(path: str) -> cv2.VideoCapture:
        """Load video to OpenCV."""
        def get_frame_length(video: cv2.VideoCapture) -> float:
            """Get number of frame in video."""
            return video.get(cv2.CAP_PROP_FRAME_COUNT)

        video: cv2.VideoCapture = cv2.VideoCapture(path)
        if get_frame_length(video) == 0:
            raise VideoFrameIsEmpty
        else:
            return video

    @staticmethod
    def __get_frame_length(video: cv2.VideoCapture) -> float:
        """Get video size as number of frames."""
        return video.get(cv2.CAP_PROP_FRAME_COUNT)

    @staticmethod
    def __each_cons(arr: list[Any], n: int) -> list[Any]:
        """Do List#each_cons(n) like Ruby."""
        return [arr[i:i+n] for i in range(len(arr)-n+1)]

    @staticmethod
    def __xor_image(im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
        "Xor 2 images."
        return cv2.bitwise_xor(im1, im2)

    @staticmethod
    def __count_moved_dots(frames: list[np.ndarray]) -> list[int]:
        """Count num of dots have moved since prev frame."""
        moved_dots = []
        for fr in frames:
            cnt = 0
            for dots in fr:
                cnt += sum(1 if x != [0, 0, 0] else 0 for x in dots.tolist())

            moved_dots.append(cnt)

        return moved_dots

    @staticmethod
    def convert_boolean_with_threshold(
            data: list[int], threshold: int = 10) -> np.ndarray:
        return np.array([(1 if i > threshold else 0)
                         for i in data])

    def detect(self,
               model: MOG = cv2.bgsegm.createBackgroundSubtractorMOG(),
               show_window: bool = True) -> list[int]:
        """Detect movement w/MOG - a background substract method by default."""
        frames: list[np.ndarray] = []
        # for reload video
        if show_window:
            xor_frames = self.__detect_with_window(frames, model)
        else:
            xor_frames = self.__detect(frames, model)

        self.processed_video = xor_frames
        dots = self.__count_moved_dots(xor_frames)

        return dots

    def __detect_with_window(
            self, frames: list[np.ndarray], model: MOG) -> list[np.ndarray]:
        ret: bool
        frame: np.ndarray
        ret, frame = self.video.read()
        while ret:
            mask = model.apply(frame)
            frame[mask == 0] = 0
            frames.append(frame)
            cv2.imshow("masked frame", frame)
            cv2.waitKey(self.__wait_sec)
            ret, frame = self.video.read()

        cv2.destroyAllWindows()

        # measure moving again
        xor_frames = []
        for x, y in self.__each_cons(frames, 2):
            f = self.__xor_image(x, y)
            xor_frames.append(f)
            cv2.imshow("xored frame", f)
            cv2.waitKey(self.__wait_sec)

        return xor_frames

    # TODO: 要高速化
    def __detect(
            self, frames: list[np.ndarray], model: MOG) -> list[np.ndarray]:
        ret, frame = self.video.read()
        while ret:
            mask = model.apply(frame)
            frame[mask == 0] = 0
            frames.append(frame)
            ret, frame = self.video.read()

        cv2.destroyAllWindows()

        # measure moving again
        xor_frames = []
        self.video.release()
        for x, y in self.__each_cons(frames, 2):
            f = self.__xor_image(x, y)
            xor_frames.append(f)

        return xor_frames

    def get_video(self) -> tuple[cv2.VideoCapture, list[np.ndarray]]:
        self.video = self.__load_video(self.video_path)
        # if hasattr(self, 'processed_video'):
        #     return (self.video, self.processed_video)
        # else:
        #     return (self.video, np.array([]))
        return (self.video, self.processed_video)


def main() -> None:
    """Main process."""
    video_path = os.path.join(
        os.path.dirname(__file__), '..',
        'videos', 'contextA.avi')

    d = DetectFreezing(video_path)
    s = input('show window?([n]/y): ')
    print('detecting...')
    if s.rstrip() == 'y':
        data = d.detect()
    else:
        data = d.detect(show_window=False)

    print('detected!')
    # import pprint
    # pprint.pprint(data, open('a.data', 'w'))
    s = input('show graph?([y]/n): ')
    if not s.rstrip() == 'n':
        print('plotting...')
        raw_video, processed_video_frames = d.get_video()
        DetectedWidget(video_path, data, raw_video, processed_video_frames)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
