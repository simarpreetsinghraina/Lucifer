
"""Conversation management for LUCIFER."""

from lucifer.core.ollama_provider import OllamaProvider
from lucifer.core.personality import LUCIFER_SYSTEM_PROMPT


class ConversationManager:
    """Manage conversation history and AI responses."""

    def __init__(
        self,
        provider: OllamaProvider | None = None,
        max_history: int = 20,
    ) -> None:
        self.provider = provider or OllamaProvider()
        self.max_history = max_history

        self.messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": LUCIFER_SYSTEM_PROMPT,
            }
        ]

    def add_user_message(self, message: str) -> None:
        """Add a user message to conversation history."""

        message = message.strip()

        if not message:
            raise ValueError("Message cannot be empty.")

        self.messages.append({
            "role": "user",
            "content": message,
        })

    def stream_response(self):
        """Generate and stream an assistant response."""

        response_parts: list[str] = []

        for token in self.provider.stream_chat(self.messages):
            response_parts.append(token)
            yield token

        response = "".join(response_parts).strip()

        if response:
            self.messages.append({
                "role": "assistant",
                "content": response,
            })

        self._trim_history()

    def _trim_history(self) -> None:
        """Keep recent conversation messages."""

        system_message = self.messages[0]

        conversation_history = self.messages[1:]

        self.messages = [
            system_message,
            *conversation_history[-self.max_history:],
        ]

    def clear_history(self) -> None:
        """Clear conversation while preserving personality."""

        self.messages = [
            {
                "role": "system",
                "content": LUCIFER_SYSTEM_PROMPT,
            }
        ]

    def get_history(self) -> list[dict[str, str]]:
        """Return a copy of conversation history."""

        return [message.copy() for message in self.messages]
