import os
import sys
import threading

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QMainWindow,
                               QPushButton, QVBoxLayout, QWidget)

import DetectedWidget
import DetectFreezing


class MainWindow(QMainWindow):

    processing = False

    def __init__(self):
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
        open_action.triggered.connect(self.open_file)

        # Exit QAction
        exit_action = QAction("Quit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage('Open video to be processed')

        self._controls()
        self._layout()

    def _controls(self):
        self.btn_detect = QPushButton('Detect', self)
        self.btn_detect.setEnabled(False)
        self.btn_detect.clicked.connect(self.detect_btn_clicked)

    def detect_btn_clicked(self):
        print('processing')
        if self.processing:
            return
        else:
            self.status.showMessage('Processing - ' + self.video_path)
            t = threading.Thread(target=self.detect(self.video_path))
            t.start()

    def _layout(self):

        self.h_box = QHBoxLayout()
        self.h_box.addWidget(self.btn_detect)

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(self.h_box)

        self.h_contents = QHBoxLayout()
        self.v_box.addLayout(self.h_contents)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.v_box)

        self.setCentralWidget(self.main_widget)

    def open_file(self):
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

    def detect(self, video):
        self.processing = True
        d = DetectFreezing.DetectFreezing(video)
        data = d.detect(show_window=False)
        self.processing = False
        self.status.showMessage('Detected - ' + self.video_path)

        # Open a result in new window
        raw_video, video_frames = d.get_video()
        sub = DetectedWidget.DetectedWidget(
            data, raw_video, video_frames, self)
        sub.show()

    @Slot()
    def exit_app(self, checked):
        sys.exit()
