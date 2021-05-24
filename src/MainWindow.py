import sys
import os

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QVBoxLayout, QWidget, QFileDialog)

import DetectFreezing

import pyqtgraph as pg

class MainWindow(QMainWindow):

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
        self.status.showMessage("Status...")

        self._controls()
        self._layout(self.btn_detect)

    def _controls(self):
        self.btn_detect = QPushButton("detect", self)
        self.btn_detect.setEnabled(False)
        self.btn_detect.clicked.connect((lambda: self.detect(self.video_path)))

    def _layout(self, cnt):

        self.h_box = QHBoxLayout()
        self.h_box.addWidget(cnt)

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(self.h_box)

        self.h_contents = QHBoxLayout()
        self.v_box.addLayout(self.h_contents)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.v_box)    
        
        self.setCentralWidget(self.main_widget)

    def open_file(self):
        name, filter = QFileDialog.getOpenFileName(
            parent=self, caption='Open File', dir=os.getcwd(), filter="View Files (*.avi)")
        print('video: ' + name)
        self.status.showMessage('video loaded - ' + name)
        self.video_path = name
        self.btn_detect.setEnabled(True)

    def detect(self, video):
        self.status.showMessage('detecting - ' + self.video_path)
        d = DetectFreezing.DetectFreezing(video)
        data = d.detect(show_window=False)

        self._layout(d.show_graph(data))


    @Slot()
    def exit_app(self, checked):
        sys.exit()

    def on_btn_clicked(self):
        print("call on_btn_clicked")

        self.lbl_contents.setText('Hello ' + self.txt_01.text())