from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


# Book
@dataclass
class Book:
    book_id: str
    author: str
    title: str
    total_copies: int
    available_copies: int

    def is_available(self) -> bool:
        return self.available_copies > 0


@dataclass
class BorrowedBooks:
    book_id: str
    borrowed_at: str


# Member
@dataclass
class Member:
    id: str
    name: str
    email: str
    active: bool
    borrowed_books: list[BorrowedBooks]

    def is_active(self) -> bool:
        return self.active

    def books_borrowed(self, book_id):
        is_borrowed: bool = False

        for book in self.borrowed_books:
            if book.book_id == book_id:
                is_borrowed = True

        return is_borrowed

# Book Borrowed
# Book Returned