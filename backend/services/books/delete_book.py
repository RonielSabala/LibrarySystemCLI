from backend.repository.book_repository import BookRepository


def delete_book_by_id(id: int) -> bool:

    repository = BookRepository()

    return repository.delete(id)
