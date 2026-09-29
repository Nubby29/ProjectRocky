import json

from rocky.brain.model import LocalModelBrain


def test_model_brain_builds_ollama_request(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            return json.dumps({"message": {"content": "Hello from Rocky."}}).encode()

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode())
        return FakeResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    brain = LocalModelBrain(model="test-model", base_url="http://localhost:11434")
    result = brain.chat("Hello", "Python is a programming language.")

    assert result.text == "Hello from Rocky."
    assert result.model == "test-model"
    assert captured["url"] == "http://localhost:11434/api/chat"
    assert captured["body"]["model"] == "test-model"
    assert captured["body"]["stream"] is False
    system = captured["body"]["messages"][0]["content"]
    assert "Python is a programming language." in system
    assert "only source of factual knowledge" in system
    assert "do not invent, infer, embellish, or guess" in system


def test_model_brain_requires_unknown_answers_to_be_explicit(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            return json.dumps({"message": {"content": "I don't know that yet."}}).encode()

    def fake_urlopen(request, timeout):
        captured["system"] = json.loads(request.data.decode())["messages"][0]["content"]
        return FakeResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    brain = LocalModelBrain(model="test-model", base_url="http://localhost:11434")
    brain.chat("Who is someone not in memory?", "[VERIFIED] Python: Python is a programming language.")

    assert "explicitly say that Rocky does not know it yet" in captured["system"]
    assert "Treat VERIFIED memory as established" in captured["system"]


def test_model_brain_chat_image_builds_vision_request(monkeypatch, tmp_path):
    captured = {}
    image = tmp_path / "rocky.png"
    image.write_bytes(b"fake-png")

    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            return json.dumps({"message": {"content": "I see an image."}}).encode()

    def fake_urlopen(request, timeout):
        captured["body"] = json.loads(request.data.decode())
        return FakeResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    monkeypatch.setenv("ROCKY_VISION_MODEL", "vision-test")
    brain = LocalModelBrain(model="test-model", base_url="http://localhost:11434")
    result = brain.chat_image("Describe this.", str(image))

    assert result.text == "I see an image."
    assert result.model == "vision-test"
    assert captured["body"]["model"] == "vision-test"
    assert captured["body"]["stream"] is False
    assert captured["body"]["messages"][1]["images"] == ["ZmFrZS1wbmc="]


def test_model_brain_normalizes_carriage_returns():
    from rocky.brain.model import clean_model_text

    assert clean_model_text("first\rsecond") == "first\nsecond"
