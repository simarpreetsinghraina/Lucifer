
"""Background AI worker for LUCIFER."""

from PySide6.QtCore import QObject, Signal, Slot

from lucifer.core.conversation import ConversationManager


class AIWorker(QObject):
    """Generate AI responses without blocking the GUI."""

    token_received = Signal(str)
    response_finished = Signal(str)
    error_occurred = Signal(str)
    finished = Signal()

    def __init__(
        self,
        conversation: ConversationManager,
    ) -> None:
        super().__init__()

        self.conversation = conversation

    @Slot()
    def run(self) -> None:
        """Generate a response and stream tokens to the UI."""

        response_parts: list[str] = []

        try:
            for token in self.conversation.stream_response():
                response_parts.append(token)
                self.token_received.emit(token)

            response = "".join(response_parts).strip()
            self.response_finished.emit(response)

        except Exception as error:
            self.error_occurred.emit(str(error))

        finally:
            self.finished.emit()
