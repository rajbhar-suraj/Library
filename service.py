from datetime import datetime, timedelta
from models import BorrowRequest, BorrowResult, Transactions, BorrowedBooks
from exceptions import (
    BookNotFoundError, MemberNotFoundError,
    MemberNotActiveError, BookNotAvailableError, BookNotBorrowedError
)
from repository import MemberRepository as Member_Repo, TransactionRepository as Transaction_Repo, BookRepository as Book_Repo
import uuid

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

    def __init__(self, book_repo, member_repo, transaction_repo):
        self.book_repo = Book_Repo
        self.member_repo = Member_Repo
        self.transaction_repo = Transaction_Repo

    def borrow_book(self, request: BorrowRequest) -> BorrowResult:
        # check if that book exist in book repo or not and its available or not
        book = self.fetch_book(request.book_id)
        self.assert_available(book)
        # check if member is legit and active or not, also check if that book is already borrowed by the customer or not
        member = self.fetch_member(request.member_id)
        self._assert_member_active(member)         # ← missing
        self._assert_not_already_borrowed(request.book_id, member)

        # record the transaction
        transaction_id=str(uuid.uuid4())

        transaction_payload = Transactions(
            id=transaction_id,
            member_id=request.member_id,
            book_id=request.book_id,
            is_penalty_applied=False,
            penalty_amt=0,
            total_amt=book.rent_price
        )

        self.record_transaction(transaction_payload)
        # hand them receipt
        receipt = BorrowResult(
            book.id,
            member.id,
            borrowed_at=datetime.now(),
            due_date= datetime.now() + timedelta(days=7),
            amt=book.rent_price
        )
        update_member_payload = BorrowedBooks(
            transaction_id,
            book.id,
            receipt.borrowed_at,
            is_return=False,
            due_date=receipt.due_date,
            total_amt=book.rent_price
        )
        # update book available qty
        self.update_book_qty(book.id, member)
        self.update_member_books(update_member_payload)
        return receipt

    def update_member_books(self, update_member_payload: BorrowedBooks):
        updated_member = self.member_repo.save(update_member_payload)
        return updated_member
    def return_book(self, member_id, book_id) ->BorrowResult:

        # 1. fetch member
        member = self.fetch_member(member_id)
        # 2. fetch book
        book = self.fetch_book(book_id)
        # 3. assert book was borrowed by this member
        is_borrowed = self._assert_not_already_borrowed(book_id, member)
        if is_borrowed: # it means the book is not borrowed look at the fn
            raise BookNotBorrowedError(book_id, member_id)


        # 4. fetch member borrowed book
        member_borrowed_book = self.fetch_borrowed_book(member, book_id)

        total_amt = member_borrowed_book.total_amt
        is_penalty = datetime.now() > member_borrowed_book.due_date
        
        if is_penalty:
            total_amt += 3

        # 5 update the transaction
        update_transaction_payload = Transactions(
            id=member_borrowed_book.id,
            member_id=member_id,
            book_id=book_id,
            is_penalty_applied=is_penalty,
            penalty_amt=3 if is_penalty else 0,
            total_amt=total_amt,
        )
        self.update_transaction(update_transaction_payload)

        # 6 update borrowed book
        update_member_payload = BorrowedBooks(
            member_borrowed_book.id,
            book.id,
            member_borrowed_book.borrowed_at,
            is_return=True,
            is_return_date=datetime.now(),
            due_date=member_borrowed_book.due_date,
            total_amt= total_amt
        )

        # 7. update book qty (operation="return")
        self.update_book_qty(book, "return")

        # update borrowed book in member
        self.update_member_books(update_member_payload)

        return BorrowResult(
            book_id=book.id,
            member_id=member_id,
            borrowed_at=member_borrowed_book.borrowed_at,
            due_date=member_borrowed_book.due_date,
            amt=total_amt
        )
        
    def fetch_borrowed_book(self, member, book_id):
        for book in member.borrowed_books:
            if book.book_id == book_id and not book.is_return:
                return book

    def update_transaction(self, transaction_payload):
        transaction = self.transaction_repo.save(transaction_payload)

        return transaction
    
    def fetch_book(self, book_id):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        return book

    def update_book_qty(self, book, operation: str):
        if operation == "borrow":
            book.available_copies -= 1
        elif operation == "return":
            book.available_copies += 1
        self.book_repo.save(book)

    def _assert_not_already_borrowed(self, book_id, member) -> bool:
        if not member.books_borrowed(book_id):
            return True
        return False

    def fetch_member(self, member_id):
        member = self.member_repo.get_by_id(member_id)
        if not member:
            raise MemberNotFoundError(member_id)
        return member   
    
    def _assert_member_active(self, member):
        if not member.active:
            raise MemberNotActiveError(member.id)
        
    def record_transaction(self,request: Transactions):
        transaction = self.transaction_repo.save(request)
        return transaction
    
