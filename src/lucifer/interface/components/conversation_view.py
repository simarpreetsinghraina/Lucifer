
"""Conversation history component for LUCIFER."""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from lucifer.interface.components.message_bubble import MessageBubble


class ConversationView(QScrollArea):
    """Display and manage the conversation message history."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the scrollable conversation area."""

        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.container = QWidget()
        self.container.setObjectName("conversationContainer")

        self.message_layout = QVBoxLayout(self.container)
        self.message_layout.setContentsMargins(12, 16, 12, 16)
        self.message_layout.setSpacing(14)
        self.message_layout.addStretch()

        self.setWidget(self.container)

        self.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QWidget#conversationContainer {
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: #294455;
                border-radius: 3px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #3B718A;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

    def add_message(self, message: str, sender: str) -> None:
        """Append a message to the conversation."""

        bubble = MessageBubble(message, sender)

        self.message_layout.insertWidget(
            self.message_layout.count() - 1,
            bubble,
            alignment=(
                Qt.AlignmentFlag.AlignRight
                if sender.lower().strip() == "user"
                else Qt.AlignmentFlag.AlignLeft
            ),
        )

        self._scroll_to_bottom()


    def _scroll_to_bottom(self) -> None:
        """Scroll to the latest message after layout updates."""

        QTimer.singleShot(
            0,
            lambda: self.verticalScrollBar().setValue(
                self.verticalScrollBar().maximum()
            ),
        )