from typing import Any, Optional

import cv2
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QGraphicsProxyWidget, QPushButton, QWidget


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
            self.frame_len = len(frames)
            return frames

    def _make_window(self) -> None:
        win = pg.GraphicsLayoutWidget(show=True)

        win.setWindowTitle('Mice Freezing Detection - processing results')
        win.resize(QSize(700, 900))

        # main graph
        freeze_graph = win.addPlot(row=0, col=0, colspan=2)
        freeze_graph.setTitle('[Freezing Graph]')
        freeze_graph.setLabel(axis='left', text='Moving Dot(s)')
        freeze_graph.setLabel(axis='bottom', text='Video Frame index')
        freeze_graph.plot(self.data)
        freeze_graph.setLimits(xMin=0, yMin=0, xMax=self.frame_len)

        win.nextRow()

        # bool graph
        bool_graph = win.addPlot(row=1, col=0, colspan=2)
        bool_graph.setRange(yRange=(0, 1), padding=0)
        bool_graph.setTitle(
            '[Freezing Boolean](1/0=T/F, th.={})'.format(self.threshold))
        bool_graph.setLabel(axis='left', text='boolean')
        bool_graph.setLabel(axis='bottom', text='Video Frame index')
        y = self.convert_boolean_with_threshold()
        bar = pg.BarGraphItem(
            x=[i for i in range(len(y))], y=y, height=1, width=0.1)
        bool_graph.addItem(bar)
        bool_graph.hideAxis('left')
        bool_graph.setLimits(xMin=0, yMin=0, xMax=self.frame_len, yMax=1)

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

        win.nextRow()

        # csv export button
        proxy = QGraphicsProxyWidget()
        button = QPushButton('Export CSV')
        proxy.setWidget(button)

        p3 = win.addLayout(row=3, col=0)
        p3.addItem(proxy, row=1, col=1)

        self.win = win

    def convert_boolean_with_threshold(self) -> list[int]:
        return [(1 if i > self.threshold else 0) for i in self.data]

    def show(self) -> None:
        try:
            self.exec()
        except AttributeError as e:
            print(type(e), 'was happened in DetectedWidget#show')
            pass
