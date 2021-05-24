import cv2
import numpy as np
import pprint
import os
import pyqtgraph as pg


class VideoFrameIsEmpty(Exception):
    pass


class DetectFreezing:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = self._load_video(video_path)
        self.__wait_sec = int(1000 / self.video.get(cv2.CAP_PROP_FPS))
        self.__video_len = self._get_frame_length(self.video)

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
    def _count_moved_dots(frames: np.ndarray) -> list:
        """Count num of dots have moved since prev frame."""
        moved_dots = []
        for fr in frames:
            cnt = 0
            for dots in fr:
                cnt += sum(1 if x != [0, 0, 0] else 0 for x in dots.tolist())

            moved_dots.append(cnt)

        return moved_dots

    def detect(self,
               model=cv2.bgsegm.createBackgroundSubtractorMOG(),
               show_window=True) -> np.ndarray:
        """Detect movement w/MOG - a background substract method by default."""
        frames = []
        ret, frame = self.video.read()
        while ret:
            mask = model.apply(frame)
            frame[mask == 0] = 0
            frames.append(frame)
            if show_window:
                cv2.imshow("masked frame", frame)
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
            if show_window:
                cv2.imshow("xored frame", f)
                cv2.waitKey(self.__wait_sec)
        else:
            # reload video file buffer
            self.video = self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.processed_video = xor_frames

        return self._count_moved_dots(xor_frames)

    def show_graph(self, data):
        # 上画面にgraph
        win = pg.GraphicsLayoutWidget(show=True)
        freeze_graph = win.addPlot()
        freeze_graph.plot(data, title="test graph")

        win.nextRow()

        # 下画面にvideo
        mice_video_frame = pg.ImageItem(self.processed_video[0])
        mice_video_frame.setImage()
        view_box = pg.ViewBox()
        view_box.addItem(mice_video_frame)
        # plot = pg.PlotItem(viewBox=view_box)
        win.addItem(view_box)
        return win
        # pg.mkQApp('Freezing Graph').exec_()



if __name__ == '__main__':
    try:
        video_path = os.path.join(os.path.dirname(__file__), '..', 'videos', 'contextA.avi')
        d = DetectFreezing(video_path)
        s = input('show window?([n]/y): ')
        print('detecting...')
        if s.rstrip() == 'y':
            data = d.detect()
        else:
            data = d.detect(show_window=False)

        print('detected!')
        # pprint.pprint(data, open('a.data', 'w'))
        s = input('show graph?([y]/n): ')
        if not s.rstrip() == 'n':
            print('plotting...')
            d.show_graph(data)
        

    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()
