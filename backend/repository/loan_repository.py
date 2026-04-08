import json
from dataclasses import dataclass, field
from datetime import datetime

from backend.common.paths import LOANS_PATH
from backend.common.utils import create_file_if_not_exists
from backend.domain import Loan
from backend.domain.enums import LoanStatusEnum


@dataclass(slots=True)
class LoanRepository:
    loans: list[Loan] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.loans = self._load()

    def _load(self) -> list[Loan]:
        if not LOANS_PATH.exists():
            return []

        with open(LOANS_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

            loaded_loans = []
            for item in data:
                item["status"] = LoanStatusEnum(item["status"])
                item["start_date"] = datetime.fromisoformat(item["start_date"])
                item["end_date"] = datetime.fromisoformat(item["end_date"])
                loaded_loans.append(Loan(**item))

            return loaded_loans

    def _save(self) -> None:
        create_file_if_not_exists(LOANS_PATH)

        with open(LOANS_PATH, "w", encoding="utf-8") as f:
            data = []
            for loan in self.loans:
                loan_dict = loan.__dict__.copy()
                loan_dict["status"] = loan.status.value
                loan_dict["start_date"] = loan.start_date.isoformat()
                loan_dict["end_date"] = loan.end_date.isoformat()
                data.append(loan_dict)

            json.dump(data, f, indent=4, ensure_ascii=False)

    def add(self, loan: Loan) -> None:
        self.loans.append(loan)
        self._save()

    def get_all(self) -> list[Loan]:
        return self.loans

    def get_by_ids(self, book_id: int, student_id: int) -> Loan | None:
        for loan in self.loans:
            if (
                loan.book_id == book_id
                and loan.student_id == student_id
                and loan.status == LoanStatusEnum.ACTIVE
            ):
                return loan

    def update(self, updated_loan: Loan) -> bool:
        for i, loan in enumerate(self.loans):
            if (
                loan.book_id != updated_loan.book_id
                or loan.student_id != updated_loan.student_id
            ):
                continue

            self.loans[i] = updated_loan
            self._save()
            return True

        return False
