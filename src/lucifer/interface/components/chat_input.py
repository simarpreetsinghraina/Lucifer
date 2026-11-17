
"""Chat input component for LUCIFER."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class ChatInput(QFrame):
    """Text input and interaction controls."""

    message_submitted = Signal(str)
    microphone_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the chat input interface."""

        self.setObjectName("chatInput")
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        self.message_field = QLineEdit()
        self.message_field.setPlaceholderText(
            "Message LUCIFER..."
        )
        self.message_field.setClearButtonEnabled(True)
        self.message_field.returnPressed.connect(
            self._submit_message
        )

        self.message_field.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #DCE7EF;
                font-size: 13px;
                padding: 8px;
            }

            QLineEdit::placeholder {
                color: #718294;
            }
        """)

        self.microphone_button = QPushButton("MIC")
        self.microphone_button.setFixedSize(44, 40)
        self.microphone_button.setToolTip(
            "Voice input (coming soon)"
        )
        self.microphone_button.clicked.connect(
            self.microphone_requested.emit
        )

        self.send_button = QPushButton("SEND")
        self.send_button.setFixedSize(64, 40)
        self.send_button.clicked.connect(
            self._submit_message
        )

        for button in (
            self.microphone_button,
            self.send_button,
        ):
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

        self.microphone_button.setStyleSheet("""
            QPushButton {
                background: #172A38;
                color: #78AFC4;
                border: 1px solid #294455;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #203B4D;
            }
        """)

        self.send_button.setStyleSheet("""
            QPushButton {
                background: #12394B;
                color: #75D8F5;
                border: 1px solid #28617A;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #19516A;
            }
        """)

        layout.addWidget(self.message_field, 1)
        layout.addWidget(self.microphone_button)
        layout.addWidget(self.send_button)

        self.setStyleSheet("""
            QFrame#chatInput {
                background: #101B27;
                border: 1px solid #294455;
                border-radius: 12px;
            }
        """)

    def _submit_message(self) -> None:
        """Emit a non-empty message and clear the input."""

        message = self.message_field.text().strip()

        if not message:
            return

        self.message_submitted.emit(message)
        self.message_field.clear()

    def set_input_enabled(self, enabled: bool) -> None:
        """Enable or disable message input."""

        self.message_field.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
