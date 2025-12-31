from domain.book.BookService import BookService
from domain.member.MemberService import MemberService
from exceptions.CustomException import (TargetBookNotFound,MemberNotFoundError,MemberIsNeverBorrowed
,BookAlreadyExists,MemberAlreadyExists,TargetBookIsBorrowed)
from repository.BookCsvRepository import BookCsvRepository
from domain.Library import Library
from domain.member.Member import Member
from domain.book.Book import Book

#BookCsvRepository에 filePath 전달
bookRepository = BookCsvRepository("../books.csv")

#현재 CSV에 저장되어 있는 데이터 가져오기
book = bookRepository.load_all()
print("[System] books.csv 에서 도서 데이터를 불러왔습니다.")

bookService = BookService(bookRepository)
memberService = MemberService({})
libraryService = Library(memberService,bookService)

#Library에 가져온 book을 생성자 주입하기
#Member를 주입하지 않는 이유는 어차피 불러올 Member가 없기 때문 (만약 MemberCsvRepository, MemberCsv가 생긴다면 주입해도 괜찮을듯)
#나중에 MemberCsvRepository도 만들어 보자

while True:
    print("=== 도서관 관리 시스템 ===")
    print("1. 도서 등록")
    print("2. 도서 목록")
    print("3. 회원 등록")
    print("4. 회원 목록")
    print("5. 대출")
    print("6. 반납")
    print("7. 검색")
    print("8. 종료")
    print("메뉴를 선택하세요: ")
    number = int(input())

    if number == 1:
        try:
            title = input("제목을 입력하세요: ")
            author = input("저자를 입력하세요: ")
            isbn = input("ISBN을 입력하세요: ")
            new_book = Book(title,author,isbn)
            bookService.add_book(new_book)
        except BookAlreadyExists:
            print(f"{e}")

    if number == 2:
        bookService.show_book()

    if number == 3:
        try:
            name = input("추가할 멤버의 이름을 입력하세요: ")
            phone = input("추가할 멤버의 휴대전화 정보를 입력하세요: ")
            new_member = Member(name,phone,[])
            memberService.add_member(new_member)
        except MemberAlreadyExists as e:
            print(f"{e}")

    if number == 4:
        memberService.show_member()

    if number == 5:
        try:
            print("[대출 시스템]")
            print("사용자 이름을 입력하세요: ")
            borrow_member_name = input()
            print("대출할 책의 ISBN을 입력하세요: ")
            borrow_isbn = input()
            libraryService.borrow_book(borrow_member_name,borrow_isbn)
        except TargetBookIsBorrowed as e:
            print(f"{e}")
    if number == 6:
        try:
            print("[반납 시스템]")
            print("반납할 사용자 이름을 입력하세요: ")
            return_member_name = input()
            print("반납할 책의 ISBN을 입력하세요: ")
            return_isbn = input()
            libraryService.return_book(return_member_name,return_isbn)
        except MemberNotFoundError as e:
            # 멤버를 찾지 못할 경우 멤버를 찾지 못했다는 익셉션 호출
            print(f"{e}")
            # 멤버가 빌린적이 없는 경우 익셉션 호출
        except MemberIsNeverBorrowed as e:
            print(f"{e}")

    if number == 7:
        try:
            isbn = input("검색할 isbn을 입력하세요: ")
            libraryService.search_book(isbn)
        except TargetBookNotFound as e:
            print(f"검색 실패 {e}")

    if number == 8:
        print("종료하겠습니다...")
        break

