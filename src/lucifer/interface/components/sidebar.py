
"""Navigation sidebar component for LUCIFER."""
from lucifer.interface.components.system_vitals import SystemVitals
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):
    """Application navigation sidebar."""

    navigation_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(235)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the sidebar interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 24, 18, 20)
        layout.setSpacing(8)

        # Brand
        brand = QLabel("LUCIFER")
        brand.setObjectName("BrandTitle")

        subtitle = QLabel("PERSONAL INTELLIGENCE")
        subtitle.setObjectName("BrandSubtitle")

        layout.addWidget(brand)
        layout.addWidget(subtitle)
        layout.addSpacing(38)

        # Navigation section
        section_label = QLabel("WORKSPACE")
        section_label.setObjectName("SectionLabel")
        layout.addWidget(section_label)
        layout.addSpacing(8)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        navigation_items = [
            ("Overview", "overview"),
            ("Conversations", "conversations"),
            ("Tasks", "tasks"),
            ("Memory", "memory"),
            ("Settings", "settings"),
        ]

        for index, (label, page_id) in enumerate(navigation_items):
            button = QPushButton(label)
            button.setObjectName("NavigationButton")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            self.button_group.addButton(button, index)
            layout.addWidget(button)

            button.clicked.connect(
                lambda _checked=False, page=page_id:
                    self._on_navigation_clicked(page)
            )

            if page_id == "overview":
                button.setChecked(True)

        layout.addSpacing(24)

        # Live system monitoring
        vitals_label = QLabel("SYSTEM VITALS")
        vitals_label.setObjectName("SectionLabel")
        layout.addWidget(vitals_label)

        self.system_vitals = SystemVitals()
        layout.addWidget(self.system_vitals)

        layout.addStretch()

        # Footer
        footer = QLabel("LUCIFER  •  DESKTOP")
        footer.setObjectName("SidebarFooter")
        layout.addWidget(footer)

        self.setStyleSheet("""
            QWidget#Sidebar {
                background-color: #111821;
                border: 1px solid #283644;
                border-radius: 12px;
            }

            QLabel#BrandTitle {
                color: #E8EEF5;
                font-size: 23px;
                font-weight: 700;
                letter-spacing: 3px;
                border: none;
            }

            QLabel#BrandSubtitle {
                color: #718294;
                font-size: 9px;
                letter-spacing: 1.5px;
                border: none;
            }

            QLabel#SectionLabel {
                color: #718294;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1.5px;
                border: none;
            }

            QLabel#PlaceholderText {
                color: #718294;
                font-size: 11px;
                padding: 8px 0;
                border: none;
            }

            QLabel#SidebarFooter {
                color: #718294;
                font-size: 9px;
                letter-spacing: 1px;
                border: none;
            }

            QPushButton#NavigationButton {
                background-color: transparent;
                color: #A0AFBE;
                border: none;
                border-radius: 7px;
                text-align: left;
                padding: 11px 12px;
                font-size: 13px;
            }

            QPushButton#NavigationButton:hover {
                background-color: #1D2A37;
                color: #E8EEF5;
            }

            QPushButton#NavigationButton:checked {
                background-color: #1B303B;
                color: #72D5E8;
                font-weight: 600;
                border-left: 3px solid #72D5E8;
            }
        """)

    def _on_navigation_clicked(self, page_id: str) -> None:
        """Emit the selected navigation destination."""

        self.navigation_requested.emit(page_id)
