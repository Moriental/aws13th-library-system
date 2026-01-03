from exceptions.CustomException import NoMatchingBooksFound
class Library:
    """
       회원 서비스와 도서 서비스를 조율하여 통합 기능을 제공하는 Library 클래스
       생성자 주입을 통해 서비스 간의 결합도를 낮출 수 있으며,
       대출, 반납, 조회와 같은 사용자 시나리오를 처리한다.
    """
    def __init__(self, member_service, book_service):
        """
        서비스 의존성을 주입받아 초기화한다.

        Argument
            :param member_service: 회원 서비스에 대한 의존성
            :param book_service: 도서 서비스에 대한 의존성
        """
        self.member_service = member_service
        self.book_service = book_service

    def borrow_book(self, member_name: str, isbn: str):
        """
        회원이 도서를 대출하는 프로세스를 수행한다.

        1. 회원 조회 -> 2. 도서 번호를 통해 해당 도서 조회 ->
        3. 도서 상태 대출로 변경 -> 4. 회원 대출 목록에 추가

        Argument:
            :param member_name: 대출할 회원의 이름
            :param isbn: 대출할 도서의 ISBN
        Return:
            :return: 대출 성공 시 True
        """
        #member_name을 이용해서 해당하는 Member 인스턴스를 가져온다.
        member = self.member_service.find_member(member_name)

        #isbn을 통해 해당하는 책을 가져오고 해당 책을 대출 상태로 바꾼다.
        target_book = self.book_service.process_borrowing_by_isbn(isbn)

        #해당 member 인스턴스에 대출할 책을 해당 member 인스턴스 리스트에서 추가한다.
        self.member_service.add_borrowed_book(member, target_book)
        print(f"{member.name}님이 {target_book.title} 책에 대출에 성공했습니다!!")
        return True

    def return_book(self, member_name: str, isbn: str):
        """
        회원이 도서를 반납하는 프로세스를 수행한다.

        1. 회원 조회 -> 2. 도서 번호를 통해 해당 도서 조회 ->
        3.도서 상태 반납으로 변경  -> 4. 회원 대출 목록에서 제거

        Argument:
            :param member_name: 반납할 회원의 이름
            :param isbn: 반납할 책의 ISBN
        Returns:
            :return: 반납 성공 시 True
        """
        #member_name을 이용해서 해당하는 Member 인스턴스를 가져온다.
        member = self.member_service.find_member(member_name)

        #isbn을 통해 해당하는 책을 가져오고 해당 책을 반납 상태로 바꾼다.
        returned_book = self.book_service.process_return_by_isbn(isbn)

        #해당 member 인스턴스에 반납할 책을 해당 member 인스턴스 리스트에서 제거한다.
        self.member_service.remove_borrowed_book(member,returned_book.isbn)
        print(f"{member.name}님의 {returned_book.title}을 반납했습니다.")
        return True

    def search_book_by_title(self, title_keyword: str):
        found_books = self.book_service.search_books_by_keyword(title_keyword)

        if not found_books:
            raise NoMatchingBooksFound(title_keyword)

        for book in found_books:
            status = "대출 중" if book.is_borrowed else "대출 가능"
            print(f"제목: {book.title} | ISBN: {book.isbn} | 상태: {status}")

        return found_books
