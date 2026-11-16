
"""Application entry point for LUCIFER."""

import sys

from PySide6.QtWidgets import QApplication

from lucifer.interface.main_window import LuciferWindow


def main() -> None:
    """Initialize and launch the application."""

    app = QApplication(sys.argv)
    app.setApplicationName("LUCIFER")

    window = LuciferWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
