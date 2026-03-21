from __future__ import annotations

import json
import shutil
from pathlib import Path

from pipeline.config import SHARED_DIRECTORIES


def shared_paths(shared_root: str | Path) -> dict[str, Path]:
    root = Path(shared_root)
    return {name: root / name for name in SHARED_DIRECTORIES}


def ensure_shared_dirs(shared_root: str | Path) -> dict[str, Path]:
    paths = shared_paths(shared_root)
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def reset_shared_dirs(shared_root: str | Path) -> dict[str, Path]:
    root = Path(shared_root)
    if root.exists():
        shutil.rmtree(root)
    return ensure_shared_dirs(root)


def write_json(path: str | Path, payload: dict) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path


def read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _stage_filename(message: dict, stage_name: str, location: str) -> str:
    transaction_id = message["data"]["transaction_id"]
    return f"{transaction_id}--{stage_name}--{location}.json"


def queue_input(shared_root: str | Path, message: dict, stage_name: str) -> Path:
    paths = ensure_shared_dirs(shared_root)
    return write_json(paths["input"] / _stage_filename(message, stage_name, "input"), message)


def move_to_processing(shared_root: str | Path, input_path: str | Path, message: dict, stage_name: str) -> Path:
    paths = ensure_shared_dirs(shared_root)
    destination = paths["processing"] / _stage_filename(message, stage_name, "processing")
    shutil.move(str(input_path), destination)
    return destination


def publish_output(shared_root: str | Path, message: dict, stage_name: str) -> Path:
    paths = ensure_shared_dirs(shared_root)
    return write_json(paths["output"] / _stage_filename(message, stage_name, "output"), message)


def archive_result(shared_root: str | Path, message: dict) -> Path:
    paths = ensure_shared_dirs(shared_root)
    transaction_id = message["data"]["transaction_id"]
    return write_json(paths["results"] / f"{transaction_id}.json", message)
