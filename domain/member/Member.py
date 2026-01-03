from dataclasses import dataclass,field


@dataclass
class Member:
    """
    회원 정보를 관리하는 데이터 클래스
        name(str) : 회원의 이름
        phone(str) : 회원의 휴대폰 번호
        borrowed_books : 회원이 빌리고 있는 도서 리스트
    """
    name: str
    phone: str
    # borrowed_list = [] 식으로 하게 되면 모든 객체가 하나의 리스트를 공유하게됨
    # 멤버 객체가 새로 생성될때마다 인스턴스에 새로운 리스트 객체를 생성하게 한다.
    borrowed_books : list = field(default_factory=list)



