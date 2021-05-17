from datetime import datetime

import cv2


class CameraIsNotWorked(Exception):
    pass


class RecordingCam():
    def __init__(self, device_id=0):
        self.camera = cv2.VideoCapture(device_id)
        if not self.camera.isOpened():
            raise CameraIsNotWorked("deviceid: " + str(device_id))

        self.video_size_info = (
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH),
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__wait_sec = int(1000 / self.camera.get(cv2.CAP_PROP_FPS))

    def rec(self, f_base="output", f_ext: str = "avi",
            frame_rate: int = 60, show_window=True) -> None:

        fname = "{}-{}.{}".format(f_base, self.make_timestamp, f_ext)
        out_file = cv2.VideoWriter(fname, -1, frame_rate, self.video_size_info)
        try:
            self._rec(out_file, show_window)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            raise e

        self.camera = self.camera.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
        out_file.release()
        cv2.destroyAllWindows()

    def _rec(self, out_file, show_window) -> None:
        ret, frame = self.video.read()
        while ret:
            # binarize frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out_file.write(frame)
            if show_window:
                cv2.imshow("masked frame", frame)
                cv2.waitKey(self.__wait_sec)

    @staticmethod
    def make_timestamp() -> str:
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')

    @staticmethod
    def check_camera(video: cv2.VideoCapture) -> bool:
        return video.isOpened()


if __name__ == '__main__':
    RecordingCam().rec()
