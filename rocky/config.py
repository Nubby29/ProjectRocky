"""Configuration for Rocky 1.0."""
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    project_root: Path
    runtime_dir: Path
    memory_file: Path
    log_file: Path
    model_name: str
    model_url: str

def load_settings(project_root: Path | None = None) -> Settings:
    root=(project_root or Path(__file__).resolve().parent.parent).resolve(); runtime=root / "runtime"
    return Settings(root,runtime,runtime/"memory.json",runtime/"rocky.log",os.getenv("ROCKY_MODEL","llama3.2:3b"),os.getenv("ROCKY_MODEL_URL","http://127.0.0.1:11434"))
