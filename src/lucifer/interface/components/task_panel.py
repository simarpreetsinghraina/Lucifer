
"""Task monitoring panel for LUCIFER."""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class TaskPanel(QWidget):
    """Display active tasks and recent activity."""

    EXPANDED_WIDTH = 300
    COLLAPSED_WIDTH = 52

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("TaskPanel")
        self.setMinimumWidth(0)
        self.setMaximumWidth(self.EXPANDED_WIDTH)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        self._is_collapsed = False

        self._setup_ui()

        self.animation = QPropertyAnimation(
            self,
            b"maximumWidth",
            self,
        )
        self.animation.setDuration(220)
        self.animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

    def _setup_ui(self) -> None:
        """Build the task panel interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 16, 12, 16)
        main_layout.setSpacing(14)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(6)

        self.header_label = QLabel("TASK ACTIVITY")
        self.header_label.setStyleSheet("""
            color: #718294;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1px;
        """)

        self.toggle_button = QPushButton("›")
        self.toggle_button.setFixedSize(28, 28)
        self.toggle_button.setCursor(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.CursorShape.PointingHandCursor
        )
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #17212C;
                color: #72D5E8;
                border: 1px solid #283644;
                border-radius: 6px;
                font-size: 18px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #1D2A37;
            }
        """)

        self.toggle_button.clicked.connect(self.toggle_panel)

        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.toggle_button)

        main_layout.addLayout(header_layout)

        # All task content lives inside this container.
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(14)

        self._add_section(content_layout, "ACTIVE TASKS")
        content_layout.addWidget(
            self._create_task_card(
                "System initialisation",
                "Running",
                72,
            )
        )

        self._add_section(content_layout, "AWAITING APPROVAL")
        content_layout.addWidget(
            self._create_task_card(
                "Install software update",
                "Approval required",
            )
        )

        self._add_section(content_layout, "RECENT ACTIVITY")
        content_layout.addWidget(
            self._create_task_card(
                "Application launched",
                "Completed",
            )
        )
        content_layout.addWidget(
            self._create_task_card(
                "Network connection",
                "Failed",
            )
        )

        content_layout.addStretch()

        main_layout.addWidget(self.content_widget)

        self.setStyleSheet("""
            QWidget#TaskPanel {
                background-color: #111821;
                border: 1px solid #283644;
                border-radius: 12px;
            }
        """)

    def _add_section(
        self,
        layout: QVBoxLayout,
        title: str,
    ) -> None:
        """Add a task section heading."""

        label = QLabel(title)
        label.setStyleSheet("""
            color: #A0AFBE;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1px;
        """)
        layout.addWidget(label)

    def _create_task_card(
        self,
        title: str,
        status: str,
        progress: int | None = None,
    ) -> QFrame:
        """Create a reusable task card."""

        card = QFrame()
        card.setObjectName("TaskCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(8)

        task_title = QLabel(title)
        task_title.setWordWrap(True)
        task_title.setStyleSheet("""
            color: #E8EEF5;
            font-size: 12px;
            font-weight: 600;
        """)
        card_layout.addWidget(task_title)

        status_label = QLabel(status)
        status_label.setStyleSheet("""
            color: #72D5E8;
            font-size: 10px;
        """)
        card_layout.addWidget(status_label)

        if progress is not None:
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(progress)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(5)
            card_layout.addWidget(progress_bar)

        card.setStyleSheet("""
            QFrame#TaskCard {
                background-color: #17212C;
                border: 1px solid #283644;
                border-radius: 8px;
            }
            QProgressBar {
                background-color: #283644;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #72D5E8;
                border-radius: 2px;
            }
        """)

        return card

    def toggle_panel(self) -> None:
        """Animate between expanded and collapsed states."""

        self.animation.stop()

        if self._is_collapsed:
            # Expand
            self.content_widget.show()
            self.header_label.show()
            self.toggle_button.setText("‹")

            start_width = self.width()
            end_width = self.EXPANDED_WIDTH

            self._is_collapsed = False

        else:
            # Collapse
            self.content_widget.hide()
            self.header_label.hide()
            self.toggle_button.setText("›")

            start_width = self.width()
            end_width = self.COLLAPSED_WIDTH

            self._is_collapsed = True

        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.start()
