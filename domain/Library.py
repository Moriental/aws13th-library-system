from .book.Book import Book  # 상대 경로를 이용해 같은 폴더 내에 있는 book 클래스 가져옴
from .member.Member import Member  # 상대 경로를 이용해 같은 폴더 내에 있는 member 클래스 가져옴
from exceptions.CustomException import MemberNotFoundError, TargetBookNotFound, TargetBookIsBorrowed, \
    MemberIsNeverBorrowed

""""
    Service Layer
"""


class Library:
    """
        생성자 주입
        :param books: 초기 도서 목록 (주입받음)
        :param members: 초기 멤버 목록 (주입받음)
    """

    def __init__(self, member_service, book_service):
        # LibraryService는 member_service와 book_service를 주입 받음
        self.member_service = member_service
        self.book_service = book_service

    # 대출 서비스 로직
    def borrow_book(self, member_name: str, isbn: str):
        member = self.member_service.find_member(member_name)

        # BookService에서 isbn으로 책을 찾는다.
        target_book = self.book_service.process_borrowing_by_isbn(isbn)
        # member 객체에 대출한 책 추가
        self.member_service.add_borrowed_book(member, target_book)
        print(f"{member.name}님이 {target_book.title} 책에 대출에 성공했습니다!!")
        return True

    def return_book(self, member_name: str, isbn: str):
        member = self.member_service.find_member(member_name)
        # 반납할 회원의 이름을 입력하세요
        # 반납할 회원의 책의 번호를 입력하세요
        borrowed_book = self.book_service.process_return_by_isbn(isbn)
        print(f"{member.name}님의 {borrowed_book.title}을 반납했습니다.")
        return True

    def search_book(self, search_book_isbn: str):
        # 책의 이름뿐만 아니라 책의 ISBN까지 같이 조회 (책의 이름은 중복될 수 있으나 ISBN은 중복되지 않음)
        find_book = self.book_service.find_books_byIsbn(search_book_isbn)

        if find_book.is_borrowed:
            print(f"{find_book.title}은 현재 도서관에 있으며 {find_book.title}은 현재 대출 중입니다.ISBN은 다음과 같습니다.{find_book.isbn}")
        else:
            print(f"{find_book.title}은 현재 도서관에 있으며 {find_book.title}은 대출 중이지 않습니다.ISBN은 다음과 같습니다.{find_book.isbn}")
        return find_book
