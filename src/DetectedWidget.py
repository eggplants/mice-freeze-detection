from typing import Any, Optional

import cv2
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget


class DetectedWidget(QWidget):
    def __init__(self, video_path: str, data: list[int],
                 raw_video: cv2.VideoCapture,
                 processed_video_frames: list[np.ndarray],
                 parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.video_path = video_path
        self.data = data
        self.raw_video = raw_video
        self.raw_video_frames = self._get_frames()
        self.processed_video_frames = processed_video_frames
        self.threshold = 30

        self._make_window()

    def _get_frames(self) -> list[np.ndarray]:
        frames: list[np.ndarray] = []
        ret: bool
        frame: np.ndarray
        ret, frame = self.raw_video.read()
        while ret:
            frames.append(frame)
            ret, frame = self.raw_video.read()
        else:
            print(len(frames))
            return frames

    def _make_window(self) -> None:
        win = pg.GraphicsLayoutWidget(show=True)

        # main graph
        freeze_graph = win.addPlot()
        freeze_graph.setTitle('[Graph]')
        freeze_graph.setLabel(axis='left', text='Y-axis')
        freeze_graph.setLabel(axis='bottom', text='X-axis')
        freeze_graph.plot(self.data)

        win.nextRow()

        # bool graph
        bool_graph = win.addPlot()
        bool_graph.setTitle('[Bool graph](th={})'.format(self.threshold))
        bool_graph.setLabel(axis='left', text='Y-axis')
        bool_graph.setLabel(axis='bottom', text='X-axis')
        y = self.convert_boolean_with_threshold()
        bar = pg.BarGraphItem(
            x=[i for i in range(len(y))], y=y, height=1, width=0.1)
        bool_graph.addItem(bar)

        win.nextRow()

        # processed video frame
        if len(self.processed_video_frames) != 0:
            mice_video_frame = pg.ImageItem(self.processed_video_frames[0])
            mice_video_frame.setImage()
            view_box = pg.ViewBox()
            view_box.addItem(mice_video_frame)
            win.addItem(view_box)

        # win.nextRow()

        # raw video frame
        if len(self.raw_video_frames) != 0:
            mice_video_frame = pg.ImageItem(self.raw_video_frames[0])
            mice_video_frame.setImage()
            view_box = pg.ViewBox()
            view_box.addItem(mice_video_frame)
            win.addItem(view_box)

        self.win = win

    def convert_boolean_with_threshold(self) -> list[int]:
        return [(0 if i > self.threshold else 1) for i in self.data]

    def show(self) -> None:
        self.exec()
