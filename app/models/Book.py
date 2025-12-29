"""
    Book 데이터 클래스 정의
"""

class Book:
    def __init__(self, title,author,isbn,is_borrowed=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def __str__(self):
        status = "대출 중" if self.is_borrowed else "대출 가능"
        return f"제목: {self.title} | 저자: {self.author} | ISBN: {self.isbn} | 상태: {status}"

