from backend.domain import Book
from backend.domain.enums import BookStatusEnum
from backend.repository.book_repository import BookRepository

def update_book_by_id(
    id: int,
    title: str | None = None,
    author_name: str | None = None,
    author_surname: str | None = None,
    category: str | None = None,
    publisher: str | None = None,
    section: int | None = None,
    status: BookStatusEnum | None = None,
) -> bool:

    repository = BookRepository()

    book = repository.get_by_id(id)

    if not book:
        return False

    updated_book = Book(
        book_id=id,
        title=title or book.title,
        author_name=author_name or book.author_name,
        author_surname=author_surname or book.author_surname,
        category=category or book.category,
        publisher=publisher or book.publisher,
        section=section if section is not None else book.section,
    )

    updated_book.status = status or book.status

    return repository.update(updated_book)
