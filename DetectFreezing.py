import cv2
import numpy as np


class VideoFrameIsEmpty(Exception):
    pass


class DetectFreezing:
    def __init__(self, video_path, show_window=True):
        self.video_path = video_path
        self.video = self._load_video(video_path)
        self.__wait_sec = int(1000 / self.video.get(cv2.CAP_PROP_FPS))
        self.__video_len = self._get_frame_length(self.video)
        self.__show_window = show_window

    # @property
    # def wait_sec(self):
    #     pass

    # @property
    # def show_window(self):
    #     pass

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
        "Xor 2 images"
        return cv2.bitwise_xor(im1, im2)

    @staticmethod
    def _show_image(image: np.ndarray, window_name: str) -> None:
        """Open window and show image"""
        cv2.imshow(window_name, image)

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

    def detect(self, model=cv2.bgsegm.createBackgroundSubtractorMOG()):
        """Detect movement w/MOG - a background substract method by default."""
        frames = []
        ret, frame = self.video.read()
        while ret:
            mask = model.apply(frame)
            frame[mask == 0] = 0
            frames.append(frame)
            if self.__show_window:
                self._show_image(frame, "masked frame")
                cv2.waitKey(self.__wait_sec)

            ret, frame = self.video.read()

        cv2.destroyAllWindows()

        # useless???
        # measure moving again
        xor_frames = []
        self.video.release()
        for x, y in self._each_cons(frames, 2):
            f = self._xor_image(x, y)
            xor_frames.append(f)
            if self.__show_window:
                self._show_image(f, "xored frame")
                cv2.waitKey(self.__wait_sec)
        else:
            # reload video file buffer
            self.video = self._load_video(self.video_path)

        return self._count_moved_dots(xor_frames)


if __name__ == '__main__':
    try:
        d = DetectFreezing("./contextA.avi")
        print(d.detect())
    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
