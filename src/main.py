import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    # exit code == PySide returned val
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("SIGINT")
    except Exception as e:
        raise e