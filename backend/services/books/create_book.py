from backend.domain import Book
from backend.repository import book_repository

def create_book(
        id: int,
        title: str,
        author_name: str,
        author_surname: str,
        category: str,
        publisher: str,
        section: int,
) -> None:
    
    repository = book_repository.BookRepository()

    if repository.get_by_id(id):
        raise ValueError(f"Book with id {id} already exists.")

    book = Book(
        book_id=id,
        title=title,
        author_name=author_name,
        author_surname=author_surname,
        category=category,
        publisher=publisher,
        section=section
    )

    repository.add(book)
