from .Book import Book # 상대 경로를 이용해 같은 폴더 내에 있는 Book 클래스 가져옴
from .Member import Member # 상대 경로를 이용해 같은 폴더 내에 있는 Member 클래스 가져옴
"""    
    Service Layer
"""
class Library:
    """
        생성자 주입
        :param books: 초기 도서 목록 (주입받음)
        :param members: 초기 멤버 목록 (주입받음)
    """
    def __init__(self,books:list[Book] = None, members:dict[str,Member] = None):
        #books에 주입 받은 데이터가 없으면 빈 컬렉션 리스트로 반환한다.
        self.books = books if books is not None else []
        #membres에 주입 받은 데이터가 없으면 빈 컬렉션 딕셔너리로 반환한다.
        self.members = members if members is not None else {}

    def add_book(self,book:Book):
        self.books.append(book)

    def add_member(self,member:Member):
        #member.name (키) member (값)
        self.members[member.name] = member

    #현재 저장되어 있는 책들을 보여주는 함수
    def show_book(self):
        if not self.books:
            print("현재 등록된 책이 없습니다.")
            return
        for book in self.books:
            print(book)

    #현재 저장되어 있는 멤버들의 목록을 보여주는 함수
    '''
        items()는 key와 value만 반환함,
        for name,phone,borrwoed_books.. (x)
        위 처럼 쓰면 안됨
        for name,member in self.members.items():
            phone = member.phone (o)
    '''
    def show_member(self):
        for name,member in self.members.items():
            phone = member.phone
            books_count = len(member.borrowed_books) # 현재 빌리고 있는 책의 개수

            #
            print(f"{name}님이 있으며 휴대폰 번호는 {phone}와 같으며 현재 빌리고 있는 책의 개수는 {books_count}개 입니다.")
    # 대출 비즈니스
    def borrow_book(self,member_name:str,isbn:str):
        member = self.members.get(member_name)
        # member를 찾을 수 없을 때 (member_name에 해당하는 객체가 없음)
        if not member:
            print("해당 회원을 찾을 수 없습니다.")
            return False

        # 리스트에서 isbn으로 책을 찾는다.
        target_book = None
        for book in self.books:
            if book.isbn == isbn:
                target_book = book
                break

        # target_book이 존재하지 않으면
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
        print(f"{member.name}님이 {target_book.title} 책에 대출에 성공했습니다!!")
        return True

    def return_book(self,member_name:str,isbn:str):
        member = self.members.get(member_name)
        # 반납할 회원의 이름을 입력하세요
        # 반납할 회원의 책의 번호를 입력하세요
        if not member: # member가 none 이라면
            print("존재하지 않는 회원입니다.")
            return False

        borrowed_book = None
        for book in member.borrowed_books:
            if book.isbn == isbn:
                borrowed_book = book
                break

        #현재 책을 빌린 기록이 없을 경우
        if not borrowed_book:
            print("책을 빌린 기록이 없습니다.")
            return False

        #현재 책이 대출 중인지 확인한다.
        if not borrowed_book.is_borrowed:
            print("현재 책은 대출중이 아닙니다.")
            return False

        borrowed_book.is_borrowed = False
        member.borrowed_books.remove(borrowed_book)
        print(f"{member.name}님의 {borrowed_book.title}을 반납했습니다.")
        return True

