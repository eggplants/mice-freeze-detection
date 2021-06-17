"""Detect moving and freezing behavior from an avi video file.
"""
import os
import sys
from typing import Any

import cv2
import numpy as np
from cv2 import bgsegm_BackgroundSubtractorMOG as MOG

from DetectedWidget import DetectedWidget


class VideoFrameIsEmpty(Exception):
    """Error raises when video frame is empty.
    """
    pass


class DetectFreezing:
    """Detect moving and freezing behavior from an avi video file.

    Raises:
        VideoFrameIsEmpty: Error raises when video frame is empty
    """

    def __init__(self, video_path: str) -> None:
        """Constructor.

        Args:
            video_path (str): video path processes
        """

        self.video_path = video_path
        self.video = self.__load_video(video_path)
        self.__wait_sec = int(1000 / self.video.get(cv2.CAP_PROP_FPS))
        self.__video_len = self.__get_frame_length(self.video)

    @staticmethod
    def __load_video(path: str) -> cv2.VideoCapture:
        """Load video to OpenCV.

        Args:
            path (str): video path

        Raises:
            VideoFrameIsEmpty: video path is invalid

        Returns:
            cv2.VideoCapture: video stream object
        """
        def get_frame_length(video: cv2.VideoCapture) -> float:
            """Get number of frame in video.

            Args:
                video (cv2.VideoCapture): video stream

            Returns:
                float: number of video frame
            """
            return video.get(cv2.CAP_PROP_FRAME_COUNT)

        video: cv2.VideoCapture = cv2.VideoCapture(path)
        if get_frame_length(video) == 0:
            raise VideoFrameIsEmpty
        else:
            return video

    @staticmethod
    def __get_frame_length(video: cv2.VideoCapture) -> float:
        """Get video size as number of frames.

        Args:
            video (cv2.VideoCapture): [description]

        Returns:
            float: [description]
        """
        return video.get(cv2.CAP_PROP_FRAME_COUNT)

    @staticmethod
    def __each_cons(arr: list[Any], n: int) -> list[Any]:
        """Do List  # each_cons(n) like Ruby.

        Args:
            arr (list[Any]): [description]
            n (int): [description]

        Returns:
            list[Any]: [description]
        """
        return [arr[i:i+n] for i in range(len(arr)-n+1)]

    @staticmethod
    def __xor_image(im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
        """Xor 2 images

        Args:
            im1 (np.ndarray): [description]
            im2 (np.ndarray): [description]

        Returns:
            np.ndarray: [description]
        """
        return cv2.bitwise_xor(im1, im2)

    @staticmethod
    def __count_moved_dots(frames: list[np.ndarray]) -> list[int]:
        """Count num of dots have moved since prev frame.

        Args:
            frames (list[np.ndarray]): [description]

        Returns:
            list[int]: [description]
        """
        moved_dots = []
        s = frames[0].shape
        for fr in frames:
            fr = fr.reshape(s[0]*s[1], s[2])

            moved_dots.append(int(np.count_nonzero(fr != [0, 0, 0])/3))

        return moved_dots

    @staticmethod
    def convert_boolean_with_threshold(
            data: list[int], threshold: int = 10) -> np.ndarray:
        """

        Args:
            data (list[int]): [description]
            threshold (int, optional): [description]. Defaults to 10.

        Returns:
            np.ndarray: [description]
        """
        return np.array([(0 if i > threshold else 1)
                         for i in data])

    def detect(self,
               model: MOG = cv2.bgsegm.createBackgroundSubtractorMOG(),
               show_window: bool = True) -> list[int]:
        """Detect movement w/MOG - a background substract method by default.

        Args:
            model (MOG, optional): [description]. Defaults to MOG.
            show_window (bool, optional): [description]. Defaults to True.

        Returns:
            list[int]: [description]
        """
        frames: list[np.ndarray] = []
        # for reload video
        if show_window:
            xor_frames = self.__detect_with_window(frames, model)
        else:
            xor_frames = self.__detect(frames, model)

        print('[counting moved dots...]', file=sys.stderr)

        self.processed_video = xor_frames
        dots = self.__count_moved_dots(xor_frames)

        return dots

    def __detect_with_window(
            self, frames: list[np.ndarray], model: MOG) -> list[np.ndarray]:
        """[summary]

        Args:
            frames (list[np.ndarray]): [description]
            model (MOG): [description]

        Returns:
            list[np.ndarray]: [description]
        """
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
        """[summary]

        Args:
            frames (list[np.ndarray]): [description]
            model (MOG): [description]

        Returns:
            list[np.ndarray]: [description]
        """
        length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        print('[length]:{} frames'.format(length), file=sys.stderr)
        if length == 0:
            return []

        ind = 0
        ret, frame = self.video.read()
        while ret:
            ind += 1
            print('[pre]:{}/{}'.format(ind, length), end='\r', file=sys.stderr)
            mask = model.apply(frame)
            frame[mask == 0] = 0
            frames.append(frame)
            ret, frame = self.video.read()
        else:
            print('\033[1K[pre]:completed!', file=sys.stderr)

        cv2.destroyAllWindows()

        # measure moving again
        xor_frames = []
        ind = 1
        self.video.release()
        for x, y in self.__each_cons(frames, 2):
            ind += 1
            print('[xor]:{}/{}'.format(ind, length), end='\r', file=sys.stderr)
            f = self.__xor_image(x, y)
            xor_frames.append(f)
        else:
            print('[xor]:completed!', file=sys.stderr)

        return xor_frames

    def get_video(self) -> tuple[cv2.VideoCapture, list[np.ndarray]]:
        """[summary]

        Returns:
            tuple[cv2.VideoCapture, list[np.ndarray]]: [description]
        """
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
    print('[detecting...]', file=sys.stderr)
    if s.rstrip() == 'y':
        data = d.detect()
    else:
        data = d.detect(show_window=False)

    print('[detected!]', file=sys.stderr)

    s = input('show graph?([y]/n): ')
    if not s.rstrip() == 'n':
        print('[plotting...]', file=sys.stderr)
        raw_video, processed_video_frames = d.get_video()
        DetectedWidget(video_path, data, raw_video, processed_video_frames)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
