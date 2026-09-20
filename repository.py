from db import get_connection
from models import Book, Member, Transactions, BorrowedBooks

class BookRepository:

    def get_by_id(self, book_id: str) -> Book | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM books WHERE id = %s",
                    (book_id,)
                )
                row = cur.fetchone()
                if not row:
                    return None
                return Book(
                    id=row["id"],
                    title=row["title"],
                    author=row["author"],
                    total_copies=row["total_copies"],
                    available_copies=row["available_copies"],
                    rent_price=row["rent_price"]
                )

    def save(self, book: Book) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (id, title, author, total_copies, available_copies, rent_price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        available_copies = EXCLUDED.available_copies
                """,
                (
                    book.id,
                    book.title,
                    book.author,
                    book.total_copies,
                    book.available_copies,
                    book.rent_price
                ))
                conn.commit()


class MemberRepository:

    def get_by_id(self, member_id: str) -> Member | None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM members WHERE id = %s",
                    (member_id,)
                )
                row = cur.fetchone()
                if not row:
                    return None

                # fetch their borrowed books too
                cur.execute(
                    "SELECT * FROM borrowed_books WHERE member_id = %s",
                    (member_id,)
                )
                borrowed_rows = cur.fetchall()
                borrowed_books = [
                    BorrowedBooks(
                        id=b["id"],
                        book_id=b["book_id"],
                        borrowed_at=b["borrowed_at"],
                        is_return=b["is_return"],
                        due_date=b["due_date"],
                        total_amt=b["total_amt"]
                    )
                    for b in borrowed_rows
                ]

                return Member(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    active=row["active"],
                    borrowed_books=borrowed_books
                )

    def save(self, borrowed_book: BorrowedBooks) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO borrowed_books
                        (id, book_id, member_id, borrowed_at, is_return, due_date, total_amt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        is_return = EXCLUDED.is_return,
                        total_amt = EXCLUDED.total_amt
                """,
                (
                    borrowed_book.id,
                    borrowed_book.book_id,
                    borrowed_book.member_id,
                    borrowed_book.borrowed_at,
                    borrowed_book.is_return,
                    borrowed_book.due_date,
                    borrowed_book.total_amt
                ))
                conn.commit()


class TransactionRepository:

    def save(self, transaction: Transactions) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO transactions
                        (id, member_id, book_id, is_penalty_applied, penalty_amt, total_amt)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        is_penalty_applied = EXCLUDED.is_penalty_applied,
                        penalty_amt        = EXCLUDED.penalty_amt,
                        total_amt          = EXCLUDED.total_amt
                """,
                (
                    transaction.id,
                    transaction.member_id,
                    transaction.book_id,
                    transaction.is_penalty_applied,
                    transaction.penalty_amt,
                    transaction.total_amt
                ))
                conn.commit()
