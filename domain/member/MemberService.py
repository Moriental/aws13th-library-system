from exceptions.CustomException import MemberAlreadyExists, MemberNotFoundError, MemberIsNeverBorrowed


class MemberService:
    def __init__(self, members: dict=None):
        if members is None:
            self.members = {}
        else:
            self.members = members

    def add_member(self, member):
        # member.name (키) member (값)
        # 폰 넘버가 중복되는 멤버가 있으면 익셉션 처리 (전화번호는 유니크 키)
        for existing_member in self.members.values():
            if existing_member.phone == member.phone:
                raise MemberAlreadyExists(member.phone)
        self.members[member.name] = member
        print(f"{member.name}님은 회원으로 성공적으로 등록이 되었습니다!")

    # 현재 저장되어 있는 멤버들의 목록을 보여주는 함수
    def show_member(self):
        if not self.members:
            print("현재 등록된 멤버가 없습니다.")
            return False

        for name, member in self.members.items():
            '''
                items()는 key와 value만 반환함,
                for name,phone,borrowed_books.. (x)'
                위 처럼 쓰면 안됨
                for name,member in self.members.items():
                phone = member.phone (o)
            '''
            phone = member.phone
            books_count = len(member.borrowed_books)  # 현재 빌리고 있는 책의 개수

            print(f"{name}님이 있으며 휴대폰 번호는 {phone}와 같으며 현재 빌리고 있는 책의 개수는 {books_count}개 입니다.")
        return True

    #member_name을 이용해서 멤버를 찾는다.
    def find_member(self,find_member_name):
        find_member = self.members.get(find_member_name)
        if not find_member:
            # 멤버를 찾을 수 없으면 NotFoundError를 반환함
            raise MemberNotFoundError(find_member_name)
        return find_member

    #member 객체에 빌린 책 리스트에 현재 책을 추가한다.
    def add_borrowed_book(self,member,book):
        member.borrowed_books.append(book)

    #member 객체에 isbn을 비교하여서 빌린 책 리스트에 책을 삭제한다.
    def remove_borrowed_book(self,member,isbn):
        for book in member.borrowed_books:
            if book.isbn == isbn:
                member.borrowed_books.remove(book)
                return True
        raise MemberIsNeverBorrowed(f"{member.name}님은 책을 빌리지 않았습니다.")