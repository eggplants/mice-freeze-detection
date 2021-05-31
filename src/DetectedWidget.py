import pyqtgraph as pg
from PySide6.QtWidgets import QWidget


class DetectedWidget(QWidget):
    def __init__(self, data, video, processed_video_frames, parent=None):
        super().__init__(parent)

        self.data = data
        self.video = video
        self.raw_video_frames = self._get_frames()
        self.processed_video_frames = processed_video_frames
        self.threshold = 30

        self._make_window()

    def _get_frames(self):
        frames = []
        ret, frame = self.video.read()
        while ret:
            frames.append(frame)
            ret, frame = self.video.read()
        else:
            print(len(frames))
            return frames

    def _make_window(self):
        win = pg.GraphicsLayoutWidget(show=True)

        # main graph
        freeze_graph = win.addPlot()
        freeze_graph.setTitle('[Graph]')
        freeze_graph.plot(self.data)

        win.nextRow()

        # bool graph
        bool_graph = win.addPlot()
        bool_graph.setTitle('[Bool graph]')
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

        # raw video frame
        if len(self.raw_video_frames) != 0:
            mice_video_frame = pg.ImageItem(self.raw_video_frames[0])
            mice_video_frame.setImage()
            view_box = pg.ViewBox()
            view_box.addItem(mice_video_frame)
            win.addItem(view_box)

        self.win = win

    def convert_boolean_with_threshold(self):
        return [(0 if i > self.threshold else 1) for i in self.data]

    def show(self):
        self.exec()
