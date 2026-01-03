from dataclasses import dataclass

"""
    타입 힌트의 공백 스타일을 PEP 8 규칙에 맞추자
    콜론(:) 뒤에 공백이 누락, PEP 8에 따르면 title:str 대신 title: str 형식
    dataclass를 사용하게 되면 __init__과 __repr__ 등 매직 메서드를 자동으로 만들어줌
    사용자 형식으로 만들고 싶으면 따로 정의해주면 됨
"""

@dataclass
class Book:
    """
    도서 정보를 관리하는 데이터 클래스
        title(str) : 도서의 제목
        author(str) : 도서의 저자
        isbn (str) : 도서 고유 번호 (유니크키)
        is_borrowed (bool) 대출 여부 (기본값:False)
    """
    title: str
    author: str
    isbn : str
    is_borrowed : bool = False # 기본값은 False 상태

    # 도서의 현재 상태를 문자열로 반환
    def __str__(self):
        #is_borrowed가 True일 경우 대출 중 -> False 일 경우 -> 대출 가능 반환
        status = "대출 중" if self.is_borrowed else "대출 가능"
        return f"제목: {self.title} | 저자: {self.author} | ISBN: {self.isbn} | 상태: {status}"

