
"""Local Ollama provider for LUCIFER."""

import json
from typing import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OllamaProvider:
    """Communicate with a locally running Ollama instance."""

    def __init__(
        self,
        model: str = "qwen3:latest",
        base_url: str = "http://127.0.0.1:11434",
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")

    def stream_chat(
        self,
        messages: list[dict[str, str]],
    ) -> Iterator[str]:
        """Stream response tokens from Ollama."""

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }

        request = Request(
            url=f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=180) as response:
                for line in response:
                    if not line.strip():
                        continue

                    data = json.loads(line.decode("utf-8"))

                    if "error" in data:
                        raise RuntimeError(data["error"])

                    content = data.get("message", {}).get(
                        "content", ""
                    )

                    if content:
                        yield content

                    if data.get("done", False):
                        break

        except HTTPError as error:
            details = error.read().decode(
                "utf-8", errors="replace"
            )
            raise RuntimeError(
                f"Ollama HTTP error {error.code}: {details}"
            ) from error

        except URLError as error:
            raise RuntimeError(
                "Cannot connect to Ollama. "
                "Make sure its local service is running."
            ) from error
