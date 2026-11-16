
"""Main window implementation for LUCIFER."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget


class LuciferWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LUCIFER")
        self.resize(1100, 700)
        self.setMinimumSize(800, 550)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Initialize the main window interface."""

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        welcome_label = QLabel("LUCIFER")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: #E6F1FF;
                font-size: 42px;
                font-weight: bold;
                letter-spacing: 8px;
            }
        """)

        layout.addWidget(welcome_label)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #10131C;
            }
        """)
