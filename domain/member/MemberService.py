from exceptions.CustomException import MemberAlreadyExists, MemberNotFoundError, MemberIsNeverBorrowed


class MemberService:
    """
        회원 가입, 조회 및 대출 도서 목록을 관리하는 서비스 클래스

        회원 이름(name)을 Key로, Member 객체를 Value로 하는 딕셔너리를 통해
        메모리 내에서 회원 데이터를 관리한다.
    """

    def __init__(self, members: dict = None):
        """
            서비스 초기화 및 기존 회원 데이터 로드,
        Argument:
            :param members (dict): 초기 회원 데이터 딕셔너리, 없을 경우 빈 딕셔너리로 시작
        """
        if members is None:
            self.members = {}
        else:
            self.members = members

    def add_member(self, member):
        """
            새로운 회원을 시스템에 등록한다.
            휴대폰 번호 중복 검사를 수행하며, 성공 시 회원 이름을 키로 저장한다.
        Argument:
            :param member (Member): 등록할 회원 객체의 인스턴스
        Raises:
            :raises MemberAlreadyExists: 이미 등록된 휴대폰 번호일 경우 발생
        """

        # member.name (키) member (값)
        # 전화번호는 시스템 내에서 유일해야 함 (Unique Key)
        for existing_member in self.members.values():
            if existing_member.phone == member.phone:
                raise MemberAlreadyExists(member.phone)

        # 이름(Name)을 활용하여 딕셔너리에 참조 저장
        self.members[member.name] = member
        print(f"{member.name}님은 회원으로 성공적으로 등록이 되었습니다!")

    # 현재 저장되어 있는 멤버들의 목록을 보여주는 함수
    def show_member(self):
        """
            현재 등록된 모든 회원의 정보와 대출 중인 도서 권수를 출력한다.
        """
        if not self.members:
            print("현재 등록된 멤버가 없습니다.")
            return False

        for name, member in self.members.items():
            '''
            참고
               items()는 key와 value만 반환함,
               for name,phone,borrowed_books.. (x) <- 이렇게 사용 x
               for name,member in self.members.items():
               phone = member.phone (o)
            '''
            books_count = len(member.borrowed_books)  # 현재 빌리고 있는 책의 개수
            print(f"{name}님이 있으며 휴대폰 번호는 {member.phone}와 같으며 현재 빌리고 있는 책의 개수는 {books_count}개 입니다.")
        return True

    # member_name을 이용해서 멤버를 찾는다.
    def find_member(self, find_member_name):
        """
            이름을 통해 회원 객체를 조회한다.
        Argument:
            :param find_member_name: 찾고자 하는 회원의 이름
        Raise:
            :raises MemberNotFoundError: 해당 이름의 회원이 존재하지 않을 경우
        Returns:
            :return: find_member (Member) : 검색된 회원 인스턴스
        """

        #member 딕셔너리에서 해당 이름의 회원을 가져옴
        find_member = self.members.get(find_member_name)
        if not find_member:
            raise MemberNotFoundError(find_member_name)
        return find_member

    # member 객체에 빌린 책 리스트에 현재 책을 추가한다.
    # 굳이 이렇게 해야 하는가 생각해보자.. 한 줄 분리를 위해서 함수를 만드는게 좋은가?..
    def add_borrowed_book(self, member, book):
        """
        Argument:
            :param member (Member): 대출 목록에 도서를 등록할 회원
            :param book (Book): 해당 책
        """
        member.borrowed_books.append(book)

    # member 객체에 isbn을 비교하여서 빌린 책 리스트에 책을 삭제한다.
    def remove_borrowed_book(self, member, isbn):
        """
        회원의 대출 목록에서 특정 ISBN을 가진 도서를 제거한다.

        Argument:
            :param member: 삭제할 회원
            :param isbn: 삭제할 책의 ISBN
        Raises:
            MemberIsNeverBorrowed: 대출 목록에서 해당 도서를 찾을 수 없을 때
        """
        for book in member.borrowed_books:
            if book.isbn == isbn:
                member.borrowed_books.remove(book)
                return True
        raise MemberIsNeverBorrowed(member.name)
