
"""Main application window for LUCIFER."""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from lucifer.interface.styles.theme import build_stylesheet


class LuciferWindow(QMainWindow):
    """Main dashboard window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LUCIFER")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        self._setup_ui()
        self.setStyleSheet(build_stylesheet())

    def _setup_ui(self) -> None:
        """Assemble the main dashboard layout."""

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Components will be added in the next steps.

        self.setCentralWidget(central_widget)
