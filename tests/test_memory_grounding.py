from pathlib import Path

from rocky.main import build_model_context
from rocky.memory.store import MemoryStore


def test_build_model_context_labels_memory_status(tmp_path: Path):
    memory = MemoryStore(tmp_path / "memory.json")
    memory.remember_fact("Jhave", "Jhave is building Rocky.")
    memory.remember_verified_fact(
        "Python",
        "Python is a programming language.",
        [{"source": "source-1"}, {"source": "source-2"}],
    )

    context = build_model_context(memory)

    assert "[LEGACY] Jhave: Jhave is building Rocky." in context
    assert "[VERIFIED] Python: Python is a programming language." in context
