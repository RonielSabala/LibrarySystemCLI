import json
from dataclasses import dataclass, field

from backend.common.paths import BOOKS_PATH
from backend.common.utils import create_file_if_not_exists
from backend.domain import Book
from backend.domain.enums import BookStatusEnum


@dataclass(slots=True)
class BookRepository:
    books: list[Book] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.books = self._load()

    def _load(self) -> list[Book]:
        if not BOOKS_PATH.exists():
            return []

        with open(BOOKS_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

            loaded_books = []
            for item in data:
                item["status"] = BookStatusEnum(item["status"])
                loaded_books.append(Book(**item))

            return loaded_books

    def _save(self) -> None:
        create_file_if_not_exists(BOOKS_PATH)

        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            data = [
                {**book.__dict__, "status": book.status.value} for book in self.books
            ]

            json.dump(data, f, indent=4, ensure_ascii=False)

    def add(self, book: Book) -> None:
        self.books.append(book)
        self._save()

    def get_all(self) -> list[Book]:
        return self.books

    def get_by_id(self, book_id: int) -> Book | None:
        for book in self.books:
            if book.book_id == book_id:
                return book

    def update(self, updated_book: Book) -> bool:
        for i, book in enumerate(self.books):
            if book.book_id != updated_book.book_id:
                continue

            self.books[i] = updated_book
            self._save()
            return True

        return False

    def delete(self, book_id: int) -> bool:
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.book_id != book_id]

        if len(self.books) < initial_length:
            self._save()
            return True

        return False
