from dataclasses import dataclass, field
from datetime import datetime

from backend.domain.enums import LoanStatusEnum


@dataclass(slots=True, kw_only=True)
class Loan:
    book_id: int
    student_id: int
    start_date: datetime = field(default_factory=datetime.now, init=False)
    end_date: datetime
    status: LoanStatusEnum = field(default=LoanStatusEnum.ACTIVE, init=False)
