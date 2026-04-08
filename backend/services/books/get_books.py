from backend.repository.book_repository import BookRepository
from backend.domain import Book


def get_all(
    book_id: int | None = None,
    book_name: str | None = None,
) -> list[Book]:

    repository = BookRepository()
    books = repository.get_all()

    if book_id is not None:
        books = [book for book in books if book.book_id == book_id]

    if book_name is not None:
        books = [
            book
            for book in books
            if book_name.lower() in book.title.lower()
        ]

    return books
