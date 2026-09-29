"""Optional local language-model brain for Rocky 1.0."""

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str


class LocalModelBrain:
    """Talk to an Ollama-compatible local chat endpoint using stdlib only."""

    def __init__(self, model: str | None = None, base_url: str | None = None, timeout: float = 60.0):
        self.model = model or os.getenv("ROCKY_MODEL", "llama3.2:3b")
        self.base_url = (base_url or os.getenv("ROCKY_MODEL_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.timeout = timeout

    def available(self) -> bool:
        try:
            request = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(request, timeout=5):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def chat(self, message: str, context: str = "") -> ModelResponse:
        message = message.strip()
        if not message:
            raise ValueError("message is required")
        system = (
            "You are Rocky, a small growing AI. Answer clearly and honestly. "
            "Use the supplied Rocky memory as the only source of factual knowledge about people, "
            "events, subjects, and the world. Do not invent, infer, embellish, or guess facts "
            "that are not supported by the supplied memory. If the user asks for information "
            "that the memory does not support, explicitly say that Rocky does not know it yet. "
            "Treat VERIFIED memory as established within Rocky's knowledge. Treat UNVERIFIED "
            "and LEGACY memory as uncertain and say so when relevant. Never turn uncertainty "
            "into a confident claim."
        )
        if context.strip():
            system += "\\n\\nRocky's current memory context:\\n" + context.strip()
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
            "stream": False,
        }).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"local model is unavailable at {self.base_url}") from exc
        text = data.get("message", {}).get("content", "").strip()
        if not text:
            raise RuntimeError("local model returned an empty response")
        return ModelResponse(text=text, model=self.model)
