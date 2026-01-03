"""
최상위 예외 클래스
"""
class LibraryError (Exception):
    pass

"""
    파일 에러 (BookCsvRepository 에러)
"""

class FileExtensionNotFound(LibraryError):
    """
        파일 저장/로드 시 확장자가 CSV가 아닐 시 익셉션 반환
    """
    def __init__(self, extension):
        self.extension = extension
        super().__init__(f"{extension}은 CSV 파일이 아닙니다.")

#FileNotFoundError는 이미 파이썬 상에서 정의된 클래스여서 오류발생
class CustomFileNotFoundError(LibraryError):
    """
        지정한 경로에 데이터 파일이 존재하지 않을 때 발생
    """
    def __init__(self,filePath):
        self.filePath = filePath
        super().__init__(f"{filePath}에 파일을 찾지 못했습니다.")

"""
    도서 관련 예외
"""
class BookError(LibraryError):
    """도서 서비스 로직 처리 중 발생하는 예외의 기본 클래스"""
    pass

class TargetBookNotFound(BookError):
    def __init__(self,target_book):
        """조회하거나 대출하려는 책이 도서관 리스트에 없을 때 발생"""
        self.target_book = target_book
        super().__init__(f"{target_book}에 책은 현재 도서관에 없습니다.")

class TargetBookIsBorrowed(BookError):
    """이미 대출 중인 도서에 대해 대출을 시도할 때 발생"""
    def __init__(self,target_book):
        self.target_book = target_book
        super().__init__(f"{target_book}은 현재 대출 중입니다.")

class BookAlreadyExists(LibraryError):
    """중복된 ISBN으로 도서를 신규 등록하려 할 때 발생"""
    def __init__(self,book):
        self.book = book
        super().__init__(f"{book.title}은 이미 책의 ISBN이 중복되어 등록이 불가능 합니다. ")

class BookIsAlreadyReturned(BookError):
    """이미 반납 처리가 되어 대출 중이 아닌 도서를 다시 반납하려 할 때 발생"""
    def __init__(self,book):
        self.book = book
        super().__init__(f"{book}은 현재 대출 중이지 않습니다.")

class NoMatchingBooksFound(BookError):
    """제목 키워드 검색 시 일치하는 도서가 한 권도 존재하지 않을 때 발생"""
    def __init__(self,title_keyword):
        self.keyword = title_keyword
        super().__init__(f"{self.keyword}에 일치하는 책을 찾을 수 없습니다. ")

"""
    멤버 관련 예외
"""

class MemberError(LibraryError):
    """회원 관리 로직 중 발생하는 예외의 기본 클래스"""
    pass

class MemberNotFoundError(MemberError):
    """이름 기반 검색 시 해당 회원이 시스템에 없을 때 발생"""
    def __init__(self, name):
        self.name = name
        super().__init__(f"{name}에 해당하는 멤버를 찾을 수 없습니다!")

class MemberIsNeverBorrowed(MemberError):
    """반납 시도 시, 해당 회원의 대출 리스트가 비어 있는 경우 발생"""
    def __init__(self,name):
        self.name = name
        super().__init__(f"{name}에 해당하는 멤버는 책을 빌린 기록이 없습니다.")

class MemberAlreadyExists(MemberError):
    """중복된 전화번호로 회원 가입을 시도할 때 발생"""
    def __init__(self,phone_number):
        self.phone_number = phone_number
        super().__init__(f"{phone_number}가 중복 됩니다.")

