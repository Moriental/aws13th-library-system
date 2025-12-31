import csv

from domain.book.Book import Book
from exceptions.CustomException import FileExtensionNotFound


class BookCsvRepository:
    # BookCsvRepository 객체를 생성할 때 filePath를 같이 넣어줘야 함
    def __init__(self, filePath: str):
        self.filePath = filePath

    def load_all(self):
        # 파일 확장자 오류 체크
        if not self.filePath.endswith(".csv"):
            raise FileExtensionNotFound(self.filePath)

        with open(self.filePath, "r", encoding="utf-8") as f:
            # books.csv에 객체들을 담을 빈 리스트
            # 생성자에 매개변수로 받게 되면 stateful 하게 되므로 데이터가 덮어 씌어질 수 있음
            # 그러므로 load_all 함수를 불러 올때마다 books 리스트 생성
            books = []

            # csv.reader는 각 줄을 리스트로 반환한다.
            reader = csv.reader(f)

            # 만약 첫 줄이 헤더 (제목,저자..와 같은 행)이라면 한 줄 건너뛴다.
            header = next(reader)

            for row in reader:
                # books 리스트에 append 할 때 각 행에 해당하는 데이터를 붙여 넣어줘야 함
                books.append(Book(row[0], row[1], row[2]))
        return books

    # 현재 메모리에 저장된 list[book]에 데이터를 가져와 "w"로 새로운 books.csv를 만든다
    def save_book(self, books: list[Book]):
        '''
            'w'모드 이므로 매번 파일을 비우고 새로 쓴다.
            즉 open(...,'w')로 파일을 열면, 파일이 이미 존재하더라도 그 내용을 전부 지우고
            0바이트 상태(빈 파일)에서 새로 시작한다. 이를 Truncate
            즉 항상 새 파일처럼 실행하는 것
            단 'a' 시에는 append 이므로 데이터를 이어 붙이므로 헤더가 두개가 생길수 있음
        '''
        if not self.filePath.endswith(".csv"):
            raise FileExtensionNotFound(self.filePath)
        with open(self.filePath, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            # [title],[author],[isbn] 헤더를 붙여 줌
            writer.writerow(["title", "author", "isbn"])

            for book in books:
                # 해당 컬럼에 열에 책에 제목 저자 isbn 추가
                writer.writerow([book.title, book.author, book.isbn])

    '''
if __name__ == "__main__": 
        테스트 코드
        repo = BookCsvRepository("../books.csv")

        # 기존에 있던 책 불러오기
        books = repo.load_all()
        print(f"추가 책 권수 {len(books)}")
    
        new_book = book("파이썬 마스터","영우","9781234567890")
        books.append(new_book)
    
        repo.save_book(books)
        print("새로운 책 추가")
    
        final_books = repo.load_all()
        print(f"추가 책 권수 {len(books)}")
    
        print(f"마지막으로 추가 된 책 제목 {final_books[-1].title}")
    '''
