from repository import BookRepository, MemberRepository, TransactionRepository
from models import BorrowRequest
from service import BookService
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from exceptions import (
    BookNotFoundError, MemberNotFoundError,
    MemberNotActiveError, BookNotAvailableError, BookNotBorrowedError
)
book_repo = BookRepository()
member_repo = MemberRepository()
transaction_repo = TransactionRepository()
service = BookService(book_repo, member_repo, transaction_repo)

router = APIRouter()

@router.post('/borrow') 
def borrow_book(payload: BorrowRequest):
    try:
        result = service.borrow_book(payload)
        return {
            "book_id":    result.book_id,
            "member_id":  result.member_id,
            "borrowed_at": result.borrowed_at,
            "due_date":   result.due_date,
            "amt":        result.amt
        }
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MemberNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MemberNotActiveError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except BookNotAvailableError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/return")
def return_book(member_id: str, book_id: str):
    try:
        result = service.return_book(member_id, book_id)
        return {
            "book_id":    result.book_id,
            "member_id":  result.member_id,
            "borrowed_at": result.borrowed_at,
            "due_date":   result.due_date,
            "amt":        result.amt
        }
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MemberNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BookNotBorrowedError as e:
        raise HTTPException(status_code=409, detail=str(e))