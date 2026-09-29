from pathlib import Path

from rocky.config import load_settings


def test_settings_paths(tmp_path: Path):
    settings = load_settings(tmp_path)
    assert settings.project_root == tmp_path.resolve()
    assert settings.memory_file == tmp_path.resolve() / "runtime" / "memory.json"
    assert settings.log_file == tmp_path.resolve() / "runtime" / "rocky.log"
