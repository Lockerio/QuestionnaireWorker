from PyQt6 import QtWidgets
from PyQt6.QtCore import QThreadPool

from desktop.runnable import Worker
from desktop.threads.create_db import create_db
from desktop.threads.download_data_and_fill_db import download_data_and_fill_db
from desktop.ui.main_window_ui import Ui_MainWindow
from desktop.ui_logger import UILogger


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Интерфейс из QTDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()

        # Необходимые переменные
        self.social_status = None
        self.departure_place = None

        self.weekdays_time_plot = [
            self.ui.mondayCheckBox_timePlot,
            self.ui.tuesdayCheckBox_timePlot,
            self.ui.wednesDayCheckBox_timePlot,
            self.ui.thursdayCheckBox_timePlot,
            self.ui.fridayCheckBox_timePlot,
            self.ui.saturdayCheckBox_timePlot,
            self.ui.sundayCheckBox_timePlot
        ]
        self.weekdays_social_status_diagram = [
            self.ui.mondayCheckBox_socialStatusDiagram,
            self.ui.tuesdayCheckBox_socialStatusDiagram,
            self.ui.wednesDayCheckBox_socialStatusDiagram,
            self.ui.thursdayCheckBox_socialStatusDiagram,
            self.ui.fridayCheckBox_socialStatusDiagram,
            self.ui.saturdayCheckBox_socialStatusDiagram,
            self.ui.sundayCheckBox_socialStatusDiagram
        ]
        self.weekdays_movement_type_diagram = [
            self.ui.mondayCheckBox_movementTypesDiagram,
            self.ui.tuesdayCheckBox_movementTypesDiagram,
            self.ui.wednesDayCheckBox_movementTypesDiagram,
            self.ui.thursdayCheckBox_movementTypesDiagram,
            self.ui.fridayCheckBox_movementTypesDiagram,
            self.ui.saturdayCheckBox_movementTypesDiagram,
            self.ui.sundayCheckBox_movementTypesDiagram
        ]

        # Кнопки
        self.ui.createDBButton.clicked.connect(self.create_db_thread)
        self.ui.downloadDataAndFillDBButton.clicked.connect(self.download_data_and_fill_db_button)

    def create_db_thread(self):
        self.print_start_thread_message()

        button = self.ui.createDBButton
        button.setEnabled(False)

        worker = Worker(create_db)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def download_data_and_fill_db_button(self):
        self.print_start_thread_message()

        button = self.ui.downloadDataAndFillDBButton
        button.setEnabled(False)

        worker = Worker(download_data_and_fill_db)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def progress_fn(self, n):
        UILogger.log_message(f"{str(n)}", self.ui.logsTextEdit)

    def print_output(self, s):
        pass

    def print_start_thread_message(self):
        UILogger.log_message("Процесс начат", self.ui.logsTextEdit)

    def thread_complete(self, button):
        button.setEnabled(True)
        UILogger.log_message("Процесс завершен", self.ui.logsTextEdit)
