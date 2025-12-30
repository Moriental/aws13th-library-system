from .Book import Book # 상대 경로를 이용해 같은 폴더 내에 있는 Book 클래스 가져옴
from .Member import Member # 상대 경로를 이용해 같은 폴더 내에 있는 Member 클래스 가져옴
from exceptions.CustomException import MemberNotFoundError, TargetBookNotFound, TargetBookIsBorrowed, \
    MemberIsNeverBorrowed, BookAlreadyExists, MemberAlreadyExists

""""
    Service Layer
"""
class Library:
    """
        생성자 주입
        :param books: 초기 도서 목록 (주입받음)
        :param members: 초기 멤버 목록 (주입받음)
    """
    def __init__(self,repo,books:list[Book] = None, members:dict[str,Member] = None):
        #books에 주입 받은 데이터가 없으면 빈 컬렉션 리스트로 반환한다.
        self.books = books if books is not None else []
        #membres에 주입 받은 데이터가 없으면 빈 컬렉션 딕셔너리로 반환한다.
        self.members = members if members is not None else {}
        self.repo = repo # main.py에서 BookCsvRepository.py 주입

    def add_book(self,new_book:Book):
        #현재 저장이 되고 있는 책의 ISBN이 중복이 되고 있는지 (ISBN은 유니크 하므로 중복 X)
        for existing_book in self.books:
            if existing_book.isbn == new_book.isbn:
                raise BookAlreadyExists(print(f"책의 ISBN이 중복되어 등록이 불가능 합니다."))

        #매우 중요!! 현재 메모리상에 추가된 book을 저장
        self.books.append(new_book)
        #book이 아닌 self.books(현재 메모리상에 저장되어 있는 book list)로
        #save_book 메소드를 호출해야 함 (안 그러면 방금 만든 book 한 객체만 추가됨)
        self.repo.save_book(self.books)
        # member.name (키) member (값)

    def add_member(self,member:Member):
        # 폰 넘버가 중복되는 멤버가 있으면 익셉션 처리 (전화번호는 유니크 키)
        for existing_member in self.members:
            raise MemberAlreadyExists(member.phone)
        self.members[member.name] = member

    #현재 메모리 상에 저장되어 있는 책들을 보여주는 함수
    def show_book(self):
        if not self.books:
            print("현재 등록된 책이 없습니다.")
            return
        for book in self.books:
            print(book)

    #현재 저장되어 있는 멤버들의 목록을 보여주는 함수
    '''
        items()는 key와 value만 반환함,
        for name,phone,borrowed_books.. (x)'
        위 처럼 쓰면 안됨
        for name,member in self.members.items():
            phone = member.phone (o)
    '''
    def show_member(self):
        for name,member in self.members.items():
            phone = member.phone
            books_count = len(member.borrowed_books) # 현재 빌리고 있는 책의 개수

            print(f"{name}님이 있으며 휴대폰 번호는 {phone}와 같으며 현재 빌리고 있는 책의 개수는 {books_count}개 입니다.")

    # 대출 서비스 로직
    def borrow_book(self,member_name:str,isbn:str):
        member = self.members.get(member_name)
        # member를 찾을 수 없을 때 (member_name에 해당하는 객체가 없음)
        if not member:
            raise MemberNotFoundError(member_name)

        # 리스트에서 isbn으로 책을 찾는다.
        target_book = None
        for book in self.books:
            if book.isbn == isbn:
                target_book = book
                break

        # target_book이 존재하지 않으면
        if not target_book:
            raise TargetBookNotFound(target_book)

        # target_book이 대출중이라면
        if target_book.is_borrowed:
            raise TargetBookIsBorrowed(target_book)

        #해당 책은 대출 상태로 전환
        target_book.is_borrowed = True
        #member 객체에 대출한 책 추가
        member.borrowed_books.append(target_book)
        print(f"{member.name}님이 {target_book.title} 책에 대출에 성공했습니다!!")
        return True

    def return_book(self,member_name:str,isbn:str):
        member = self.members.get(member_name)
        # 반납할 회원의 이름을 입력하세요
        # 반납할 회원의 책의 번호를 입력하세요
        if not member: # member가 none 이라면
            raise MemberNotFoundError(member.name)

        borrowed_book = None
        for book in member.borrowed_books:
            if book.isbn == isbn:
                borrowed_book = book
                break

        #현재 책을 빌린 기록이 없을 경우
        if not borrowed_book:
            raise MemberIsNeverBorrowed(member.name)

        # 현재 책이 대출 중인지 확인한다. (필요 없는 중복 코드)
        # if not borrowed_book.is_borrowed:
        #     print("현재 책은 대출중이 아닙니다.")
        #     return False

        borrowed_book.is_borrowed = False
        member.borrowed_books.remove(borrowed_book)
        print(f"{member.name}님의 {borrowed_book.title}을 반납했습니다.")
        return True

    def search_book(self,search_book_title:str,search_book_isbn:str):
        #책의 이름뿐만 아니라 책의 ISBN까지 같이 조회 (책의 이름은 중복될 수 있으나 ISBN은 중복되지 않음)
        find_book = None
        for book in self.books:
            # 만약 책의 이름을 잘못 치더라도 ISBN이 맞으면 조회 가능 (그 반대 경우도 가능)
            if book.title == search_book_title or book.isbn == search_book_isbn:
                find_book= book
                break

        # 해당하는 책을 찾을 수 없을 때
        if not find_book:
            raise TargetBookNotFound(search_book_title)

        if find_book.is_borrowed:
            print(f"{find_book.title}은 현재 도서관에 있으며 {find_book.title}은 현재 대출 중입니다.ISBN은 다음과 같습니다.{find_book.isbn}")
        else:
            print(f"{find_book.title}은 현재 도서관에 있으며 {find_book.title}은 대출 중이지 않습니다.ISBN은 다음과 같습니다.{find_book.isbn}")
        return find_book
