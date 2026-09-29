from pathlib import Path

from rocky.memory.store import MemoryStore


def test_missing_memory_returns_empty_structure(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    assert store.load() == {"facts": [], "experiences": []}


def test_memory_round_trip(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    data = {"facts": [{"text": "1 + 1 = 2"}], "experiences": []}
    store.save(data)
    assert store.load() == data
