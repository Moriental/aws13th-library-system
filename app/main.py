from exceptions.CustomException import (TargetBookNotFound,MemberNotFoundError,MemberIsNeverBorrowed
,BookAlreadyExists,MemberAlreadyExists)
from repository.BookCsvRepository import BookCsvRepository
from domain.Library import Library
from domain.Member import Member
from domain.Book import Book

#BookCsvRepository에 filePath 전달
bookRepository = BookCsvRepository("../books.csv")

#현재 CSV에 저장되어 있는 데이터 가져오기
book = bookRepository.load_all()
print("[System] books.csv 에서 도서 데이터를 불러왔습니다.")

#Library에 가져온 book을 생성자 주입하기
#Member를 주입하지 않는 이유는 어차피 불러올 Member가 없기 때문 (만약 MemberCsvRepository, MemberCsv가 생긴다면 주입해도 괜찮을듯)
#나중에 MemberCsvRepository도 만들어 보자
LibraryService = Library(bookRepository,book)

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
            title,author,isbn = map(input("제목, 저자, isbn을 공백으로 구분하여 입력하세요: ").split())
            new_book = Book(title,author,isbn)
            LibraryService.add_book(new_book)
        except BookAlreadyExists:
            print(f"{e}")

    if number == 2:
        LibraryService.show_book()

    if number == 3:
        try:
            name,phone = map(input("이름과 폰 번호를 공백으로 구분하여 입력하세요:").split())
            new_member = Member(name,phone,[])
            LibraryService.add_member(new_member)
        except MemberAlreadyExists:
            print(f"{e}")
        # 테스트 코드
        # for i in range(3):
        #     new_member = Member("kim", "010-2342-3453",[])
        #     LibraryService.add_member(new_member)

    if number == 4:
        LibraryService.show_member()

    if number == 5:
        print("[대출 시스템]")
        print("사용자 이름을 입력하세요: ")
        borrow_member_name = input()
        print("대출할 책의 ISBN을 입력하세요: ")
        borrow_isbn = input()
        LibraryService.borrow_book(borrow_member_name,borrow_isbn)

    if number == 6:
        try:
            print("[반납 시스템]")
            print("반납할 사용자 이름을 입력하세요: ")
            return_member_name = input()
            print("반납할 책의 ISBN을 입력하세요: ")
            return_isbn = input()
            LibraryService.return_book(return_member_name,return_isbn)
        except MemberNotFoundError as e:
            print(f"{e}")
        except MemberIsNeverBorrowed as e:
            print(f"{e}")

    if number == 7:
        try:
            title = input("검색할 책의 제목을 입력하세요:")
            isbn = input("검색할 isbn을 입력하세요: ")
            LibraryService.search_book(title,isbn)
        except TargetBookNotFound as e:
            print(f"검색 실패 {e}")

    if number == 8:
        print("종료하겠습니다...")
        break

