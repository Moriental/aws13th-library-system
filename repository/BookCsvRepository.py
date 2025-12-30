import csv

from domain.Book import Book


class BookCsvRepository:
    # BookCsvRepository 객체를 생성할 때 filePath를 같이 넣어줘야 함
    def __init__(self,filePath:str):
        self.filePath = filePath

    def load_all(self):
        with open(self.filePath,"r",encoding="utf-8") as f:
            # books.csv에 객체들을 담을 빈 리스트
            # 생성자에 생성을 하게 되면 stateful 하게 되므로 데이터가 덮어 씌어질 수 있음
            # load_all 함수를 불러 올때마다 books 리스트 생성
            books = []

            #csv.reader는 각 줄을 리스트로 반환한다.
            reader = csv.reader(f)

            # 만약 첫 줄이 헤더 (제목,저자..와 같은 행)이라면 한 줄 건너뛴다.
            header= next(reader)

            for row in reader:
                #books 리스트에 append 할 때 각 행에 해당하는 데이터를 붙여 넣어줘야 함
                books.append(Book(row[0],row[1],row[2]))

            #출력 되는지 테스트용
            #for book in books:
            #    print(book)
            return books

    def save_book(self,books:list[Book]):
        with open("../books.csv","w",encoding="utf-8") as f:
            writer = csv.writer(f)

if __name__ == "__main__":
    book = BookCsvRepository("../books.csv")
    books = book.load_all()