import json
from dataclasses import dataclass, field

from backend.common.paths import BOOKS_PATH
from backend.common.utils import create_file_if_not_exists
from backend.domain import Book
from backend.domain.enums import BookStatusEnum


def _book_to_dict(book: Book) -> dict:
    """Serializa un Book a dict compatible con JSON.

    No se usa __dict__ porque Book tiene slots=True y por tanto
    los objetos no poseen atributo __dict__.
    """
    return {
        "book_id":        book.book_id,
        "title":          book.title,
        "author_name":    book.author_name,
        "author_surname": book.author_surname,
        "category":       book.category,
        "publisher":      book.publisher,
        "section":        book.section,
        "status":         book.status.value,
    }


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
                # status tiene init=False en Book, hay que asignarlo aparte
                status = BookStatusEnum(item.pop("status"))
                book = Book(**item)
                book.status = status
                loaded_books.append(book)

            return loaded_books

    def _save(self) -> None:
        create_file_if_not_exists(BOOKS_PATH)

        with open(BOOKS_PATH, "w", encoding="utf-8") as f:
            json.dump(
                [_book_to_dict(b) for b in self.books],
                f,
                indent=4,
                ensure_ascii=False,
            )

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
