import traceback

from PyQt6 import QtWidgets
from PyQt6.QtCore import QThreadPool, Qt, QSize
from PyQt6.QtWidgets import QVBoxLayout
from matplotlib.figure import Figure

from app.scripts.db_to_df import get_df_from_db
from desktop.questionnaires_analyzer import QuestionnairesAnalyzer
from desktop.runnable import Worker
from desktop.threads.create_db import create_db
from desktop.threads.download_data_and_fill_db import download_data_and_fill_db
from desktop.ui.main_window_ui import Ui_MainWindow
from desktop.mpl_canvas import MplCanvas
from desktop.utils.questionnaire_filtration_helper import QuestionnaireFiltrationHelper
from desktop.utils.ui_logger import UILogger


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Интерфейс из QTDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Интерфейс для графиков
        self.time_plot_figure = Figure()
        self.social_status_diagram_figure = Figure()
        self.movement_type_diagram_figure = Figure()

        self.time_plot_canvas = MplCanvas(self.time_plot_figure, self)
        self.social_status_diagram_canvas = MplCanvas(self.social_status_diagram_figure, self)
        self.movement_type_diagram_canvas = MplCanvas(self.movement_type_diagram_figure, self)

        time_plot_layout = QVBoxLayout()
        social_status_diagram_layout = QVBoxLayout()
        movement_type_diagram_layout = QVBoxLayout()

        time_plot_layout.addWidget(self.time_plot_canvas)
        social_status_diagram_layout.addWidget(self.social_status_diagram_canvas)
        movement_type_diagram_layout.addWidget(self.movement_type_diagram_canvas)

        self.ui.timePlotWidget.setLayout(time_plot_layout)
        self.ui.socialStatusDiagramWidget.setLayout(social_status_diagram_layout)
        self.ui.movementTypesDiagramWidget.setLayout(movement_type_diagram_layout)

        # Необходимые переменные
        self.threadpool = QThreadPool()

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

        try:
            self.df = get_df_from_db()
        except:
            self.df = None

        # Кнопки
        self.ui.createDBButton.clicked.connect(self.create_db_thread)
        self.ui.downloadDataAndFillDBButton.clicked.connect(self.download_data_and_fill_db_button)

        self.ui.buildTimePlotButton.clicked.connect(self.build_time_plot)
        self.ui.buildSocialStatusDiagramButton.clicked.connect(self.build_social_status_diagram)
        self.ui.buildMovementTypesDiagramButton.clicked.connect(self.build_movement_types_diagram)



    def create_db_thread(self):
        self.print_start_thread_message()

        button = self.ui.createDBButton
        button.setEnabled(False)

        worker = Worker(create_db)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def download_data_and_fill_db_button(self):
        self.print_start_thread_message()

        button = self.ui.downloadDataAndFillDBButton
        button.setEnabled(False)

        worker = Worker(download_data_and_fill_db)
        worker.signals.result.connect(self.set_df)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def build_time_plot(self):
        social_status = QuestionnaireFiltrationHelper.get_active_radiobutton([
            self.ui.employeeRadioButton_timePlot,
            self.ui.StudentRadioButton_timePlot,
            self.ui.OthersRadioButton_timePlot,
        ])

        if social_status:
            social_status = social_status.text()
        else:
            social_status = None

        departure_place = QuestionnaireFiltrationHelper.get_active_radiobutton([
            self.ui.homeRadioButton_timePlot,
            self.ui.JobRadioButton_timePlot,
            self.ui.EducationRadioButton_timePlot,
        ])

        if departure_place:
            departure_place = departure_place.text()
        else:
            departure_place = None

        weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.weekdays_time_plot)

        if weekdays:
            weekdays = list(map(lambda rb: rb.text().lower(), weekdays))
            print(weekdays)
        else:
            weekdays = None

        figure = QuestionnairesAnalyzer.get_hours_plot_figure(self.df, social_status, departure_place, weekdays)

        self.time_plot_figure.clear()
        self.time_plot_figure = figure

        self.time_plot_canvas.figure = self.time_plot_figure
        self.time_plot_canvas.draw()

        plot_widget_size = self.ui.timePlotWidget.size()
        new_width = int(plot_widget_size.width())
        new_height = int(plot_widget_size.height())
        self.time_plot_canvas.resize(QSize(new_width, new_height))

    def build_social_status_diagram(self):
        weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.weekdays_social_status_diagram)

        if weekdays:
            weekdays = map(lambda rb: rb.text().lower(), weekdays)
        else:
            weekdays = None

        figure = QuestionnairesAnalyzer.get_people_pie_diagram_figure(self.df, weekdays)

        self.social_status_diagram_figure.clear()
        self.social_status_diagram_figure = figure

        self.social_status_diagram_canvas.figure = self.social_status_diagram_figure
        self.social_status_diagram_canvas.draw()

        plot_widget_size = self.ui.timePlotWidget.size()
        new_width = int(plot_widget_size.width())
        new_height = int(plot_widget_size.height())
        self.social_status_diagram_canvas.resize(QSize(new_width, new_height))

    def build_movement_types_diagram(self):
        weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.weekdays_movement_type_diagram)

        if weekdays:
            weekdays = map(lambda rb: rb.text().lower(), weekdays)
        else:
            weekdays = None

        figure = QuestionnairesAnalyzer.get_types_pie_diagram_figure(self.df, weekdays)

        self.movement_type_diagram_figure.clear()
        self.movement_type_diagram_figure = figure

        self.movement_type_diagram_canvas.figure = self.movement_type_diagram_figure
        self.movement_type_diagram_canvas.draw()

        plot_widget_size = self.ui.timePlotWidget.size()
        new_width = int(plot_widget_size.width())
        new_height = int(plot_widget_size.height())
        self.movement_type_diagram_canvas.resize(QSize(new_width, new_height))

    def progress_fn(self, n):
        UILogger.log_message(f"{str(n)}", self.ui.logsTextEdit)

    def set_df(self, s):
        self.df = s

    def print_start_thread_message(self):
        UILogger.log_message("Процесс начат", self.ui.logsTextEdit)

    def thread_complete(self, button):
        button.setEnabled(True)
        UILogger.log_message("Процесс завершен", self.ui.logsTextEdit)
