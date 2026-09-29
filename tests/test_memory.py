from pathlib import Path

from rocky.memory.store import MemoryStore


def test_missing_memory_creates_empty_file(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    assert store.load() == {"facts": [], "experiences": []}
    assert (tmp_path / "memory.json").exists()


def test_memory_round_trip(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    data = {"facts": [{"text": "1 + 1 = 2"}], "experiences": []}
    store.save(data)
    assert store.load() == data


def test_remember_and_find_fact(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    store.remember_fact("Jhave", "Jhave is the owner of Rocky.")

    assert store.find_facts("jhave") == [
        {"subject": "Jhave", "text": "Jhave is the owner of Rocky."}
    ]


def test_remember_replaces_same_subject(tmp_path: Path):
    store = MemoryStore(tmp_path / "memory.json")
    store.remember_fact("Rocky", "Version 0.2")
    store.remember_fact("rocky", "Version 0.2.1")

    assert store.find_facts("ROCKY") == [
        {"subject": "rocky", "text": "Version 0.2.1"}
    ]
