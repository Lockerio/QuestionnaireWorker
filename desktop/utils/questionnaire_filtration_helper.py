from typing import List

from PyQt6.QtWidgets import QRadioButton, QCheckBox


class QuestionnaireFiltrationHelper:
    @staticmethod
    def get_active_radiobutton(radiobuttons: List[QRadioButton]):
        for radiobutton in radiobuttons:
            if radiobutton.isChecked():
                return radiobutton
        return None

    @staticmethod
    def get_weekdays(checkboxes: List[QCheckBox]):
        weekdays = []
        for checkbox in checkboxes:
            if checkbox.isChecked():
                weekdays.append(checkbox)
        return weekdays
