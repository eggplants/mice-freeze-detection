import sys

from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow  # type: ignore

BANNER = '''\
           _                 __
 _ __ ___ (_) ___ ___       / _|_ __ ___  ___ _______
| '_ ` _ \\| |/ __/ _ \\_____| |_| '__/ _ \\/ _ \\_  / _ \\_____
| | | | | | | (_|  __/_____|  _| | |  __/  __// /  __/_____|
|_| |_| |_|_|\\___\\___|     |_| |_|  \\___|\\___/___\\___|

     _      _            _   _
  __| | ___| |_ ___  ___| |_(_) ___  _ __
 / _` |/ _ \\ __/ _ \\/ __| __| |/ _ \\| '_ \\
| (_| |  __/ ||  __/ (__| |_| | (_) | | | |
 \\__,_|\\___|\\__\\___|\\___|\\__|_|\\___/|_| |_|'''


def main() -> None:
    """Launch main window from MainWindow.py.
    """
    print(BANNER)
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
