from datetime import datetime

from PyQt6.QtWidgets import QPlainTextEdit


class UILogger:
    @staticmethod
    def log_message(message: str, text_area: QPlainTextEdit, level: str = "info"):
        log_message = f"<{datetime.now()}> - {level.upper()}: {message}"
        text_area.appendPlainText(log_message)
