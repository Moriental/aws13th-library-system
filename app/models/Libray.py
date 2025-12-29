from .Book import Book # 상대 경로를 이용해 같은 폴더 내에 있는 Book 클래스 가져옴
from .Member import Member # 상대 경로를 이용해 같은 폴더 내에 있는 Member 클래스 가져옴

class Library():
    def __init__(self):
        #book 객체를 담을 리스트
        self.books = []
        #Member 객체들을 담을 딕셔너리
        self.members = {}

    def add_book(self,book:Book.Book):
        self.books.append(book)

    def add_member(self,member:Member.Member):
        #member 객체를 인자로 받아 딕셔너리에 추가한다.
        self.members[member.name] = member

    def borrow_book(self,member_name,isbn):
        member = self.members.get(member_name)
        # java에서 !if 표현
        if not member:
            print("해당 회원을 찾을 수 없습니다.")
            return False

        # 리스트에서 isbn으로 책을 찾는다.
        target_book = None
        for book in self.books:
            if book.isbn == isbn:
                target_book = book
                break

        # target_book은 None인가? 만약 None 이라면
        if not target_book:
            print(f"{isbn}에 해당하는 책을 찾을 수 없습니다!")
            return False
        # target_book이 대출중이라면
        if target_book.is_borrowed:
            print(f"{isbn}에 해당하는 책은 이미 대출중입니다.")
            return False

        #해당 책은 대출 상태로 전환
        target_book.is_borrowed = True

        #member 객체에 대출한 책 추가
        member.borrowed_books.append(target_book)

        return True

    def return_book(self):
        return True