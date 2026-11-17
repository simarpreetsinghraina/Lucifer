
"""Main application window for LUCIFER."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from lucifer.interface.components.orb import LuciferOrb
from lucifer.interface.components.sidebar import Sidebar
from lucifer.interface.components.task_panel import TaskPanel
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
        main_layout.setSpacing(18)

        # Left navigation and system vitals
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Central workspace
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)

        workspace_layout.setContentsMargins(20, 20, 20, 20)
        workspace_layout.setSpacing(12)

        # Animated energy orb
        self.orb = LuciferOrb()
        self.orb.setFixedSize(420, 420)

        workspace_layout.addStretch()

        workspace_layout.addWidget(
            self.orb,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # Orb status
        self.orb_status = QLabel("SYSTEM STANDBY")
        self.orb_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb_status.setStyleSheet("""
            color: #718294;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 2px;
        """)

        workspace_layout.addWidget(self.orb_status)

        # Temporary orb state testing controls
        self.state_selector = QComboBox()
        self.state_selector.addItems([
            "Idle",
            "Listening",
            "Thinking",
            "Speaking",
            "Executing",
            "Error",
            "Offline",
        ])

        self.state_selector.currentTextChanged.connect(
            self._change_orb_state
        )

        workspace_layout.addWidget(
            self.state_selector,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        workspace_layout.addStretch()

        main_layout.addWidget(workspace, 1)

        # Right task monitoring panel
        self.task_panel = TaskPanel()
        main_layout.addWidget(self.task_panel)

        self.setCentralWidget(central_widget)

    def _change_orb_state(self, state: str) -> None:
        """Temporarily change the orb state for testing."""

        state_id = state.lower()

        self.orb.set_state(state_id)
        self.orb_status.setText(state.upper())
