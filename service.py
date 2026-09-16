from datetime import datetime
from .models import BorrowRequest, BorrowResult
from .exceptions import (
    BookNotFoundError, MemberNotFoundError,
    MemberInactiveError, BookNotAvailableError, BookNotBorrowedError
)

# Book Borrowed
# @dataclass
# class BorrowRequest:
#     book_id:str
#     member_id: string

# # Book Result
# @dataclass
# class BorrowResult:
#     book_id:str
#     member_id:str
#     borrowed_at: datetime 
class BookService:

    def __init__(self, book_repo, member_repo):
        self.book_repo = book_repo
        self.member_repo = member_repo

    def borrow_book(self, request: BorrowRequest) -> BorrowResult:
        
        pass

    def return_book(self, member_id, book_id) ->BorrowResult:
        pass
def return_book():

    # check if member exist and book exist in or not in our record
    # check if that book was borrowed by that member or not
    # if book was returned before due date or not(add penalty)
    # record the transaction
    # hand them receipt
    # update book qty
    pass
