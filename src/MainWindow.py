import os
import sys
from typing import Optional

import pyqtgraph as pg
from PySide6.QtCore import QSize, Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMainWindow,
                               QPushButton, QVBoxLayout, QWidget)

from DetectedWidget import DetectedWidget
from DetectFreezing import DetectFreezing


class Worker(QThread):
    """[summary]

    Args:
        QThread ([type]): [description]
    """
    rtn = Signal(tuple, name='rtn')

    def __init__(self, video_path: Optional[str] = None) -> None:
        """[summary]

        Args:
            video_path (Optional[str], optional): [description]. Defaults to None.
        """
        super(Worker, self).__init__()
        self.video_path = video_path

    def run(self) -> None:
        """[summary]
        """
        d: DetectFreezing
        d = DetectFreezing(self.video_path)
        data: list[int] = d.detect(show_window=False)
        res = (d, data)
        self.rtn.emit(res)


class MainWindow(QMainWindow):
    """[summary]

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self) -> None:
        """[summary]
        """
        QMainWindow.__init__(self)
        self.setWindowTitle("Mice Freezing Detection")
        self.resize(QSize(500, 400))

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Open File QAction
        open_action = QAction("Open video...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip('Open video')
        open_action.triggered.connect(self.__open_file)

        # Exit QAction
        exit_action = QAction("Quit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage('Please open video to be processed')

        self._controls()
        self._layout()

        self.setFixedHeight(200)
        self.setFixedWidth(500)

    def _controls(self) -> None:
        """Define control UI.
        """
        self.btn_detect = QPushButton('Detect', self)
        self.btn_detect.setEnabled(False)
        self.btn_detect.clicked.connect(self.__detect_btn_clicked)

        self.btn_open = QPushButton('Open video...', self)
        self.btn_open.clicked.connect(self.__open_file)

    def __detect_btn_clicked(self) -> None:
        """Executes to process when button clicked
        """
        print('processing')
        if not self.worker.isRunning():
            self.status.showMessage('Wait... - ' + self.video_path)
            self.btn_detect.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.worker.start()

    def _layout(self) -> None:
        """Define layout UI
        """
        self.h_box1 = QHBoxLayout()
        label1 = QLabel(self)
        label1.setText(
            '<div align="center">mice-freeze-detection</div>')
        self.h_box1.addWidget(label1)

        self.h_box = QHBoxLayout()
        self.h_box.addWidget(self.btn_detect)
        self.h_box.addWidget(self.btn_open)

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(self.h_box1)
        self.v_box.addLayout(self.h_box)

        self.h_contents = QHBoxLayout()
        self.v_box.addLayout(self.h_contents)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.v_box)

        self.setCentralWidget(self.main_widget)

    def __open_file(self) -> None:
        """Open video file with file explorer.
        """
        name: str
        filter: str
        name, filter = QFileDialog.getOpenFileName(
            parent=self, caption='Open File',
            dir=os.getcwd(), filter="View Files (*.avi)")
        print('video: ' + name)
        if name == '':
            self.status.showMessage('Open video to be processed')
            self.video_path = name
            self.btn_detect.setEnabled(False)
        else:
            self.status.showMessage('Loaded - ' + name)
            self.video_path = name
            self.btn_detect.setEnabled(True)

        self.worker: QThread = Worker(self.video_path)
        self.worker.rtn.connect(self.__detected)

    def __detected(self,
                   result: tuple[DetectFreezing, list[int]]) -> None:
        """Open a window which results are plotted

        Args:
            result (tuple[DetectFreezing, list[int]]): [description]
        """
        self.status.showMessage('Processed - ' + self.video_path)
        self.btn_detect.setEnabled(True)
        self.btn_open.setEnabled(True)
        d, data = result
        raw_video, video_frames = d.get_video()
        sub = DetectedWidget(
            self.video_path, data, raw_video, video_frames, self)
        sub.show()

    @Slot()
    def exit_app(self, _: bool) -> None:
        """Close app.

        Args:
            _ (bool): placeholder
        """
        sys.exit()
