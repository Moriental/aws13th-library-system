from exceptions.CustomException import BookAlreadyExists, TargetBookNotFound,TargetBookIsBorrowed,BookIsAlreadyReturned


class BookService:
    def __init__(self,book_csv_repository):
        #main.py에서 book_csv_repository 의존성 주입
        self.book_csv_repository = book_csv_repository
        #books에 현재 메모리에 저장된 도서 목록 불러오기
        self.books = book_csv_repository.load_all()

    #현재 메모리 상에 저장되어 있는 책들을 보여주는 함수
    def show_book(self):
        if not self.books:
            print("현재 등록된 책이 없습니다.")
            return
        for book in self.books:
            print(book)

    def add_book(self,new_book):
        #현재 저장이 되고 있는 책의 ISBN이 중복이 되고 있는지 (ISBN은 유니크 하므로 중복 X)
        for existing_book in self.books:
            if existing_book.isbn == new_book.isbn:
                raise BookAlreadyExists(f"책의 ISBN이 중복되어 등록이 불가능 합니다.")

        #매우 중요!! 현재 메모리상에 추가된 book을 저장
        self.books.append(new_book)
        #book이 아닌 self.books(현재 메모리상에 저장되어 있는 book list)로
        #save_book 메소드를 호출해야 함 (안 그러면 방금 만든 book 한 객체만 추가됨)
        self.book_csv_repository.save_book(self.books)
        # member.name (키) member (값)

    def find_books_byIsbn(self,search_book_isbn):
        find_book = None
        for book in self.books:
            if book.isbn == search_book_isbn:
                find_book = book
                return find_book
        raise TargetBookNotFound(search_book_isbn)

    #isbn을 통해 해당 책이 반납 상태인지 확인하고 해당 책을 사용자에게 대출 전환
    def process_borrowing_by_isbn(self,isbn):
        # target_book이 대출중이라면
        target_book = self.find_books_byIsbn(isbn)
        if target_book.is_borrowed:
            raise TargetBookIsBorrowed(target_book)

        # 해당 책은 대출 상태로 전환
        target_book.is_borrowed = True
        return target_book

    #책 반납 시 해당 책이 대출 상태인지 확인하고 해당 책을 사용자에게 반납
    def process_return_by_isbn(self,isbn):
        target_book = self.find_books_byIsbn(isbn)
        if not target_book.is_borrowed:
            raise BookIsAlreadyReturned(f"{target_book.title}은 이미 반납중입니다.")

        target_book.is_borrowed = False
        return target_book