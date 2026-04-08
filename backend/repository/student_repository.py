import json
from dataclasses import field

from backend.common.paths import STUDENTS_PATH
from backend.common.utils import create_file_if_not_exists
from backend.domain import Student


class StudentRepository:
    students: list[Student] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.students = self._load()

    def _load(self) -> list[Student]:
        if not STUDENTS_PATH.exists():
            return []

        with open(STUDENTS_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Student(**item) for item in data]

            except json.JSONDecodeError:
                return []

    def _save(self) -> None:
        create_file_if_not_exists(STUDENTS_PATH)

        with open(STUDENTS_PATH, "w", encoding="utf-8") as f:
            data = [student.__dict__ for student in self.students]
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add(self, student: Student) -> None:
        self.students.append(student)
        self._save()

    def get_all(self) -> list[Student]:
        return self.students

    def get_by_id(self, student_id: int) -> Student | None:
        for student in self.students:
            if student.student_id == student_id:
                return student
