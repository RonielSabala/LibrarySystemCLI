from pathlib import Path
from typing import Final

_ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Final[Path] = _ROOT_DIR / "data"

# Data
BOOKS_PATH: Final[Path] = DATA_DIR / "books.json"
LOANS_PATH: Final[Path] = DATA_DIR / "loans.json"
STUDENTS_PATH: Final[Path] = DATA_DIR / "students.json"
