from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


# Book
@dataclass
class Book:
    id: str
    author: str
    title: str
    total_copies: int
    available_copies: int
    rent_price: int

    def is_available(self) -> bool:
        return self.available_copies > 0


@dataclass
class BorrowedBooks:
    id: str
    book_id: str        # ← add this
    borrowed_at: datetime
    is_return: bool
    id_returned_date: datetime
    due_date: datetime
    total_amt: int



@dataclass
class Transactions:
    id: str
    member_id: str
    book_id: str
    is_penalty_applied: bool
    penalty_amt: int
    total_amt: int
    is_return: bool

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
            if book.book_id == book_id and not book.is_return:
                is_borrowed = True

        return is_borrowed

# Book Borrowed
@dataclass
class BorrowRequest:
    book_id:str
    member_id: str

# Book Result
@dataclass
class BorrowResult:
    book_id:str
    member_id:str
    borrowed_at: datetime 
    due_date: datetime
    amt: int

