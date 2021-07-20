from datetime import datetime

import cv2
import numpy as np


class CameraIsNotWorked(Exception):
    """Error for handing not to work a camera.
    """
    pass


class RecordingCam():
    """Recording camera.
    """

    def __init__(self, device_id: int = 0) -> None:
        """[summary]

        Args:
            device_id (int, optional): [description]. Defaults to 0.

        Raises:
            CameraIsNotWorked: [description]
        """
        self.camera = cv2.VideoCapture(device_id)
        if not self.camera.isOpened():
            raise CameraIsNotWorked("deviceid: " + str(device_id))

        self.video_size_info = (
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH),
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__wait_sec = int(1000 / self.camera.get(cv2.CAP_PROP_FPS))
        print(self.video_size_info, self.__wait_sec)

    @staticmethod
    def get_camid_list() -> list[int]:
        """Get a list of ids of camera device.

        Returns:
            list[int]: list of cam ids.
        """
        from itertools import count
        ids = []
        for i in count():
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                ids.append(i)
            else:
                break
            cap.release()
        return ids

    def rec(self, f_base: str = "output", f_ext: str = "avi",
            frame_rate: int = 60, show_window: bool = True) -> None:
        """Recording with camera.

        Args:
            f_base (str, optional): file base dir. Defaults to "output".
            f_ext (str, optional): file extension. Defaults to "avi".
            frame_rate (int, optional): recording frame rate. Defaults to 60.
            show_window (bool, optional): flag if window shows or not. Defaults to True.

        Raises:
            Exception: unexpected error while recoring.
        """
        fname = "{}-{}.{}".format(f_base, self.make_timestamp, f_ext)
        out_file: cv2.VideoWriter = cv2.VideoWriter(
            fname, -1, frame_rate, self.video_size_info)
        try:
            self._rec(out_file, show_window)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            raise e

        self.camera = self.camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
        out_file.release()
        cv2.destroyAllWindows()

    def _rec(self, out_file: cv2.VideoWriter, show_window: bool) -> None:
        """Recoring helper.

        Args:
            out_file (cv2.VideoWriter): output file object.
            show_window (bool):  flag if window shows or not.
        """
        ret: bool
        frame: np.ndarray
        ret, frame = self.camera.read()
        while ret:
            # binarize frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out_file.write(frame)
            if show_window:
                cv2.imshow("masked frame", frame)
                cv2.waitKey(self.__wait_sec)

    @staticmethod
    def make_timestamp() -> str:
        """Make a string of timestamp.

        Returns:
            str: timestamp ('%Y-%m-%d_%H-%M-%S_%f').
        """
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')

    @staticmethod
    def check_camera(video: cv2.VideoCapture) -> bool:
        """Check if a camera is ok.

        Args:
            video (cv2.VideoCapture): video object.

        Returns:
            bool: if camera is ok or not.
        """
        return video.isOpened()


if __name__ == '__main__':
    lis = RecordingCam.get_camid_list()
    print('available cams: ', lis)
    cam_id = int(input('gemmie id:'))
    if cam_id in lis:
        RecordingCam(cam_id).rec()
