"""Configuration for Rocky 0.1."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Application paths and runtime settings."""

    project_root: Path
    runtime_dir: Path
    memory_file: Path
    log_file: Path


def load_settings(project_root: Path | None = None) -> Settings:
    root = (project_root or Path(__file__).resolve().parent.parent).resolve()
    runtime = root / "runtime"
    return Settings(
        project_root=root,
        runtime_dir=runtime,
        memory_file=runtime / "memory.json",
        log_file=runtime / "rocky.log",
    )
