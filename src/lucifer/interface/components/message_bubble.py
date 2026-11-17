
"""Reusable message bubble component for LUCIFER."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class MessageBubble(QFrame):
    """Display an individual user or assistant message."""

    def __init__(
        self,
        message: str,
        sender: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.message = message
        self.sender = sender.lower().strip()

        if self.sender not in {"user", "lucifer"}:
            raise ValueError(
                "sender must be either 'user' or 'lucifer'"
            )

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Build the message bubble."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        sender_label = QLabel(
            "YOU" if self.sender == "user" else "LUCIFER"
        )

        sender_label.setStyleSheet("""
            color: #62C8E8;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.5px;
            background: transparent;
        """)

        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        message_label.setStyleSheet("""
            color: #DCE7EF;
            font-size: 13px;
            background: transparent;
        """)

        layout.addWidget(sender_label)
        layout.addWidget(message_label)

        if self.sender == "user":
            self.setStyleSheet("""
                MessageBubble {
                    background-color: #142A39;
                    border: 1px solid #23465A;
                    border-radius: 12px;
                }
            """)
        else:
            self.setStyleSheet("""
                MessageBubble {
                    background-color: #101B27;
                    border: 1px solid #1C3545;
                    border-radius: 12px;
                }
            """)
