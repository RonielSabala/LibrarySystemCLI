from pathlib import Path

from backend.common.paths import DATA_DIR


def create_file_if_not_exists(path: Path) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
