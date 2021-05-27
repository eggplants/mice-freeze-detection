import os

import cv2
import numpy as np


class VideoFrameIsEmpty(Exception):
    pass


class DetectFreezing:
    """Detect moving and freezing behavior from an avi video file."""

    def __init__(self, video_path):
        self.video_path = video_path
        self.video = self._load_video(video_path)
        self.__wait_sec = int(1000 / self.video.get(cv2.CAP_PROP_FPS))
        self.__video_len = self._get_frame_length(self.video)

    @staticmethod
    def _load_video(path: str) -> cv2.VideoCapture:
        """Load video to OpenCV."""
        def get_frame_length(video: cv2.VideoCapture) -> float:
            """Get number of frame in video."""
            return video.get(cv2.CAP_PROP_FRAME_COUNT)

        video = cv2.VideoCapture(path)
        if get_frame_length(video) == 0:
            raise VideoFrameIsEmpty
        else:
            return video

    @staticmethod
    def _get_frame_length(video: cv2.VideoCapture) -> float:
        """Get video size as number of frames."""
        return video.get(cv2.CAP_PROP_FRAME_COUNT)

    @staticmethod
    def _each_cons(arr: list, n: int) -> list:
        """Do List#each_cons(n) like Ruby."""
        return [arr[i:i+n] for i in range(len(arr)-n+1)]

    @staticmethod
    def _xor_image(im1: np.ndarray, im2: np.ndarray) -> np.ndarray:
        "Xor 2 images."
        return cv2.bitwise_xor(im1, im2)

    @staticmethod
    def _count_moved_dots(frames: np.ndarray) -> list:
        """Count num of dots have moved since prev frame."""
        moved_dots = []
        for fr in frames:
            cnt = 0
            for dots in fr:
                cnt += sum(1 if x != [0, 0, 0] else 0 for x in dots.tolist())

            moved_dots.append(cnt)

        return moved_dots

    def convert_boolean_with_threshold(self, threshold: int):
        return np.array([(0 if i > threshold else 1)
                         for i in self.data])

    def detect(self,
               model=cv2.bgsegm.createBackgroundSubtractorMOG(),
               show_window=True) -> np.ndarray:
        """Detect movement w/MOG - a background substract method by default."""
        frames = []
        # for reload video
        if show_window:
            xor_frames = self._detect_with_window(frames, model)
        else:
            xor_frames = self._detect(frames, model)

        self.processed_video = xor_frames
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return self._count_moved_dots(xor_frames)

    def _detect_with_window(self, frames, model):
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
        self.video.release()
        for x, y in self._each_cons(frames, 2):
            f = self._xor_image(x, y)
            xor_frames.append(f)
            cv2.imshow("xored frame", f)
            cv2.waitKey(self.__wait_sec)

        return xor_frames

    # TODO: 要高速化
    def _detect(self, frames, model):
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
        for x, y in self._each_cons(frames, 2):
            f = self._xor_image(x, y)
            xor_frames.append(f)

        return xor_frames

    def get_video(self):
        if hasattr(self, 'processed_video'):
            return (self.video, self.processed_video)
        else:
            return (self.video, None)


if __name__ == '__main__':
    try:
        video_path = os.path.join(os.path.dirname(
            __file__), '..', 'videos', 'contextA.avi')
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
            import DetectedWidget
            print('plotting...')
            DetectedWidget.DetectedWidget(
                data, *d.get_video())

    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
