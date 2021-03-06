from .DetectFreezing import DetectFreezing as DetectFreezing
from .DetectedWidget import DetectedWidget as DetectedWidget
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow
from typing import Any, Optional

class Worker(QThread):
    rtn: Any = ...
    video_path: Any = ...
    def __init__(self, video_path: Optional[str]=...) -> None: ...
    def run(self) -> None: ...

class MainWindow(QMainWindow):
    menu: Any = ...
    file_menu: Any = ...
    status: Any = ...
    def __init__(self) -> None: ...
    def detect_btn_clicked(self) -> None: ...
    video_path: Any = ...
    worker: Any = ...
    def open_file(self) -> None: ...
    def detect(self, result: tuple[Df, list[int]]) -> None: ...
    def exit_app(self, checked: Any) -> None: ...
