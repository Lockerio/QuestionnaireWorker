import sys
from PyQt6 import QtWidgets

from desktop.window.main_window import MainWindow


def app():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


app()
