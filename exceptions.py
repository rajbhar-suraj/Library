

class LibraryError(Exception):
    """Base for all library errors."""


class MemberNotFoundError(LibraryError):
    def __init__(self, member_id: str):
        self.member_id = member_id
        super().__init__(f"{member_id}: Member not found")

class MemberNotActiveError(LibraryError):

    def __init__(self, member_id):
        self.member_id = self.member_id
        super().__init__(f"{member_id}: Member not active")

class BookNotFoundError(LibraryError):

    def __init__(self, book_id):
        self.book_id = book_id
        super().__init_(f"{book_id}: Book not found")

class BookNotAvailableError(LibraryError):

    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"{book_id}: Book not available")

class BookNotBorrowedError(LibraryError):

    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"{book_id}: Book not borrowed")

