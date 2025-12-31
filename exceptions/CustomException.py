# 도서관 시스템의 최상위 에러
class LibraryError (Exception):
    pass

"""
    파일 에러 (BookCsvRepository 에러)
"""
class FileExtensionNotFound(LibraryError):
    def __init__(self, extension):
        self.extension = extension
        super().__init__(f"{extension}은 CSV 파일이 아닙니다.")

class FileNotFoundError(LibraryError):
    def __init__(self):
        super().__init__(f"파일을 찾지 못했습니다.")

"""
    도서 관련 예외
"""
class BookError(LibraryError):
    pass

class TargetBookNotFound(BookError):
    def __init__(self,target_book):
        self.target_book = target_book
        super().__init__(f"{target_book}에 책은 현재 도서관에 없습니다.")

class TargetBookIsBorrowed(BookError):
    def __init__(self,target_book):
        self.target_book = target_book
        super().__init__(f"{target_book}은 현재 대출 중입니다.")

class BookAlreadyExists(LibraryError):
    def __init__(self,book):
        self.book = book

class BookIsAlreadyReturned(BookError):
    def __init__(self,book):
        self.book = book
        super().__init__(f"{book}은 현재 대출 중이지 않습니다.")
"""
    멤버 관련 예외
"""

class MemberError(LibraryError):
    pass

class MemberNotFoundError(MemberError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"{name}에 해당하는 멤버를 찾을 수 없습니다!")

class MemberIsNeverBorrowed(MemberError):
    def __init__(self,name):
        self.name = name
        super().__init__(f"{name}에 해당하는 멤버는 책을 빌린 기록이 없습니다.")

class MemberAlreadyExists(MemberError):
    def __init__(self,phone_number):
        self.phone_number = phone_number
        super().__init__(f"{phone_number}가 중복 됩니다.")

