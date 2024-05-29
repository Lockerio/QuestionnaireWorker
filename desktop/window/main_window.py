import geopandas
from PyQt6 import QtWidgets
from PyQt6.QtCore import QThreadPool, QSize, QStringListModel
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QFileDialog
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.figure import Figure

from app.df_to_list import df_to_list
from app.get_data_by_shape import get_data_by_shape
from app.scripts.db_to_df import get_df_from_db
from app.questionnaires_filtration import QuestionnaireFiltration
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

        time_plot_toolbar = NavigationToolbar2QT(self.time_plot_canvas, self)
        social_status_diagram_toolbar = NavigationToolbar2QT(self.social_status_diagram_canvas, self)
        movement_type_diagram_toolbar = NavigationToolbar2QT(self.movement_type_diagram_canvas, self)

        time_plot_layout = QVBoxLayout()
        social_status_diagram_layout = QVBoxLayout()
        movement_type_diagram_layout = QVBoxLayout()

        time_plot_layout.addWidget(self.time_plot_canvas)
        time_plot_layout.addWidget(time_plot_toolbar)
        social_status_diagram_layout.addWidget(self.social_status_diagram_canvas)
        social_status_diagram_layout.addWidget(social_status_diagram_toolbar)
        movement_type_diagram_layout.addWidget(self.movement_type_diagram_canvas)
        movement_type_diagram_layout.addWidget(movement_type_diagram_toolbar)

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
        ]
        self.weekends_time_plot = [
            self.ui.saturdayCheckBox_timePlot,
            self.ui.sundayCheckBox_timePlot
        ]
        self.general_weekdays_time_plot = self.weekdays_time_plot + self.weekends_time_plot

        self.weekdays_social_status_diagram = [
            self.ui.mondayCheckBox_socialStatusDiagram,
            self.ui.tuesdayCheckBox_socialStatusDiagram,
            self.ui.wednesDayCheckBox_socialStatusDiagram,
            self.ui.thursdayCheckBox_socialStatusDiagram,
            self.ui.fridayCheckBox_socialStatusDiagram,
        ]
        self.weekends_social_status_diagram = [
            self.ui.saturdayCheckBox_socialStatusDiagram,
            self.ui.sundayCheckBox_socialStatusDiagram
        ]
        self.general_weekdays_social_status_diagram = self.weekdays_social_status_diagram + self.weekends_social_status_diagram

        self.weekdays_movement_type_diagram = [
            self.ui.mondayCheckBox_movementTypesDiagram,
            self.ui.tuesdayCheckBox_movementTypesDiagram,
            self.ui.wednesDayCheckBox_movementTypesDiagram,
            self.ui.thursdayCheckBox_movementTypesDiagram,
            self.ui.fridayCheckBox_movementTypesDiagram,
        ]
        self.weekends_movement_type_diagram = [
            self.ui.saturdayCheckBox_movementTypesDiagram,
            self.ui.sundayCheckBox_movementTypesDiagram
        ]
        self.general_weekdays_movement_type_diagram = self.weekdays_movement_type_diagram + self.weekends_movement_type_diagram

        try:
            self.df = get_df_from_db()
            self.fill_list_view()
        except:
            self.df = None
            UILogger.log_message("База данных не создана", self.ui.logsTextEdit)

        # Кнопки
        self.ui.createDBButton.clicked.connect(self.create_db_thread)
        self.ui.downloadDataAndFillDBButton.clicked.connect(self.download_data_and_fill_db_thread)

        self.ui.buildTimePlotButton.clicked.connect(self.build_time_plot)
        self.ui.buildSocialStatusDiagramButton.clicked.connect(self.build_social_status_diagram)
        self.ui.buildMovementTypesDiagramButton.clicked.connect(self.build_movement_types_diagram)

        self.ui.resetFiltersPushButton.clicked.connect(self.reset_time_plot_filters)
        self.ui.resetFiltersPushButton_socialStatusDiagram.clicked.connect(self.reset_social_status_diagram_filters)
        self.ui.resetFiltersPushButton_movementTypesDiagram.clicked.connect(self.reset_movement_types_diagram_filters)

        self.ui.uploadShapeFileButton.clicked.connect(
            lambda: self.show_file_dialog(self.ui.filepathToShapeFile)
        )

        # Фильтрация
        self.ui.weekdaysRadioButton_timePlot.toggled.connect(lambda: self.fill_weekdays_radiobutton(
            self.weekdays_time_plot,
            self.weekends_time_plot,
        ))
        self.ui.weekendsRadioButton_timePlot.toggled.connect(lambda: self.fill_weekends_radiobutton(
            self.weekdays_time_plot,
            self.weekends_time_plot,
        ))
        self.ui.CustomWeekdaysRadioButton_timePlot.toggled.connect(lambda: self.set_custom_weekdays(
            self.general_weekdays_time_plot
        ))

        self.ui.weekdaysRadioButton_socialStatusDiagram.toggled.connect(lambda: self.fill_weekdays_radiobutton(
            self.weekdays_social_status_diagram,
            self.weekends_social_status_diagram
        ))
        self.ui.weekendsRadioButton_socialStatusDiagram.toggled.connect(lambda: self.fill_weekends_radiobutton(
            self.weekdays_social_status_diagram,
            self.weekends_social_status_diagram
        ))
        self.ui.CustomWeekdaysRadioButton_socialStatusDiagram.toggled.connect(lambda: self.set_custom_weekdays(
            self.general_weekdays_social_status_diagram
        ))

        self.ui.weekdaysRadioButton_movementTypesDiagram.toggled.connect(lambda: self.fill_weekdays_radiobutton(
            self.weekdays_movement_type_diagram,
            self.weekends_movement_type_diagram
        ))
        self.ui.weekendsRadioButton_movementTypesDiagram.toggled.connect(lambda: self.fill_weekends_radiobutton(
            self.weekdays_movement_type_diagram,
            self.weekends_movement_type_diagram
        ))
        self.ui.CustomWeekdaysRadioButton_movementTypesDiagram.toggled.connect(lambda: self.set_custom_weekdays(
            self.general_weekdays_movement_type_diagram
        ))

        # Функции, выполняющиеся при инициализации программы
        self.reset_time_plot_filters()
        self.reset_social_status_diagram_filters()
        self.reset_movement_types_diagram_filters()

    def create_db_thread(self):
        self.print_start_thread_message()

        button = self.ui.createDBButton
        button.setEnabled(False)

        worker = Worker(create_db)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def download_data_and_fill_db_thread(self):
        self.print_start_thread_message()

        button = self.ui.downloadDataAndFillDBButton
        button.setEnabled(False)

        worker = Worker(download_data_and_fill_db)
        worker.signals.result.connect(self.set_df)
        worker.signals.finished.connect(lambda: self.thread_complete(button))
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

    def build_time_plot(self):
        try:
            shape = geopandas.read_file(self.ui.filepathToShapeFile.text())
            self.df = get_data_by_shape(self.df, shape, "lat", "lon")
        except:
            pass

        try:
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

            weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.general_weekdays_time_plot)

            if weekdays:
                weekdays = list(map(lambda rb: rb.text().lower(), weekdays))
            else:
                weekdays = None

            figure = QuestionnaireFiltration.get_hours_plot_figure(self.df, social_status, departure_place, weekdays)

            self.time_plot_figure.clear()
            self.time_plot_figure = figure

            self.time_plot_canvas.figure = self.time_plot_figure
            self.time_plot_canvas.draw()

            plot_widget_size = self.ui.timePlotWidget.size()
            new_width = int(plot_widget_size.width())
            new_height = int(plot_widget_size.height())
            self.time_plot_canvas.resize(QSize(new_width, new_height))

        except:
            pass

    def build_social_status_diagram(self):
        try:
            shape = geopandas.read_file(self.ui.filepathToShapeFile.text())
            self.df = get_data_by_shape(self.df, shape, "lat", "lon")
        except:
            pass

        try:
            weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.general_weekdays_social_status_diagram)

            if weekdays:
                weekdays = map(lambda rb: rb.text().lower(), weekdays)
            else:
                weekdays = None

            figure = QuestionnaireFiltration.get_people_pie_diagram_figure(self.df, weekdays)

            self.social_status_diagram_figure.clear()
            self.social_status_diagram_figure = figure

            self.social_status_diagram_canvas.figure = self.social_status_diagram_figure
            self.social_status_diagram_canvas.draw()

            plot_widget_size = self.ui.timePlotWidget.size()
            new_width = int(plot_widget_size.width())
            new_height = int(plot_widget_size.height())
            self.social_status_diagram_canvas.resize(QSize(new_width, new_height))
        except:
            pass

    def build_movement_types_diagram(self):
        try:
            shape = geopandas.read_file(self.ui.filepathToShapeFile.text())
            self.df = get_data_by_shape(self.df, shape, "lat", "lon")
        except:
            pass

        try:
            weekdays = QuestionnaireFiltrationHelper.get_weekdays(self.general_weekdays_movement_type_diagram)

            if weekdays:
                weekdays = map(lambda rb: rb.text().lower(), weekdays)
            else:
                weekdays = None

            figure = QuestionnaireFiltration.get_types_pie_diagram_figure(self.df, weekdays)

            self.movement_type_diagram_figure.clear()
            self.movement_type_diagram_figure = figure

            self.movement_type_diagram_canvas.figure = self.movement_type_diagram_figure
            self.movement_type_diagram_canvas.draw()

            plot_widget_size = self.ui.timePlotWidget.size()
            new_width = int(plot_widget_size.width())
            new_height = int(plot_widget_size.height())
            self.movement_type_diagram_canvas.resize(QSize(new_width, new_height))
        except:
            pass

    def progress_fn(self, n):
        UILogger.log_message(f"{str(n)}", self.ui.logsTextEdit)

    def set_df(self, s):
        self.df = s
        self.fill_list_view()

    def print_start_thread_message(self):
        UILogger.log_message("Процесс начат", self.ui.logsTextEdit)

    def thread_complete(self, button):
        button.setEnabled(True)
        UILogger.log_message("Процесс завершен", self.ui.logsTextEdit)

    def fill_weekdays_radiobutton(self, weekdays, weekends):
        for weekday in weekdays:
            weekday.setChecked(True)

        for weekend in weekends:
            weekend.setChecked(False)

        for weekday in weekdays + weekends:
            weekday.setEnabled(False)

    def fill_weekends_radiobutton(self, weekdays, weekends):
        for weekday in weekdays:
            weekday.setChecked(False)

        for weekend in weekends:
            weekend.setChecked(True)

        for weekday in weekdays + weekends:
            weekday.setEnabled(False)

    def set_custom_weekdays(self, weekdays):
        for weekday in weekdays:
            weekday.setChecked(False)
            weekday.setEnabled(True)

    def reset_time_plot_filters(self):
        self.ui.employeeRadioButton_timePlot.setAutoExclusive(False)
        self.ui.StudentRadioButton_timePlot.setAutoExclusive(False)
        self.ui.OthersRadioButton_timePlot.setAutoExclusive(False)
        self.ui.employeeRadioButton_timePlot.setChecked(False)
        self.ui.StudentRadioButton_timePlot.setChecked(False)
        self.ui.OthersRadioButton_timePlot.setChecked(False)
        self.ui.employeeRadioButton_timePlot.setAutoExclusive(True)
        self.ui.StudentRadioButton_timePlot.setAutoExclusive(True)
        self.ui.OthersRadioButton_timePlot.setAutoExclusive(True)

        self.ui.homeRadioButton_timePlot.setAutoExclusive(False)
        self.ui.JobRadioButton_timePlot.setAutoExclusive(False)
        self.ui.EducationRadioButton_timePlot.setAutoExclusive(False)
        self.ui.homeRadioButton_timePlot.setChecked(False)
        self.ui.JobRadioButton_timePlot.setChecked(False)
        self.ui.EducationRadioButton_timePlot.setChecked(False)
        self.ui.homeRadioButton_timePlot.setAutoExclusive(True)
        self.ui.JobRadioButton_timePlot.setAutoExclusive(True)
        self.ui.EducationRadioButton_timePlot.setAutoExclusive(True)

        self.ui.CustomWeekdaysRadioButton_timePlot.setChecked(True)

    def reset_social_status_diagram_filters(self):
        self.ui.CustomWeekdaysRadioButton_socialStatusDiagram.setChecked(True)

    def reset_movement_types_diagram_filters(self):
        self.ui.CustomWeekdaysRadioButton_movementTypesDiagram.setChecked(True)

    def fill_list_view(self):
        model = QStringListModel()
        list_from_df = df_to_list(self.df)
        model.setStringList(list_from_df)
        self.ui.DBPrewiewListView.setModel(model)

    def show_file_dialog(self, text_field: QLineEdit):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*)")
        if file_name:
            text_field.setText(file_name)
