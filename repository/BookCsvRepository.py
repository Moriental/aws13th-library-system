import csv

from domain.book.Book import Book
from exceptions.CustomException import FileExtensionNotFound, CustomFileNotFoundError

"""
    CSV 파일을 통해 도서 데이터를 영구 저장하고 로드하는 저장소 클래스
    데이터 저장소와 메모리 객체 (Book 인스턴스)간의 상호작용을 담당함
"""
class BookCsvRepository:
    # BookCsvRepository 객체를 생성할 때 filePath를 같이 넣어줘야 함
    def __init__(self, filePath: str):
        """
        저장소 초기화 및 CSV 파일 경로 설정
        Argument:
            :param filePath: 도서 데이터가 저장된 CSV 파일의 상대 또는 절대 경로
        """
        self.filePath = filePath

    def load_all(self):
        """
        CSV 파일의 모든 데이터를 읽어서 Book 객체 리스트로 반환한다.

        동작 방식:
        1. 확장자 및 파일 존재 여부 검증
        2. 헤더 (첫 줄)을 제외한 데이터 행을 순회하며 Book 인스턴스 생성
        3. 빈 파일일 경우 빈 리스트 반환
        Returns:
            :return:
        Raises:
            :raise FileExtensionNotFound: 파일 확장자가 .csv 파일이 아닐 때
            :raise CustomFileNotFoundError: 지정된 경로에 파일이 없을 경우
        """
        # 파일 확장자 오류 체크
        if not self.filePath.endswith(".csv"):
            raise FileExtensionNotFound(self.filePath)

        # 파일 존재 여부 및 읽기 시도
        try:
            # 파일을 수동으로 열어보고 에러가 없으면 context manager(with)로 넘긴다.
            f = open(self.filePath, "r", encoding="utf-8", newline='')
        except FileNotFoundError:
            raise CustomFileNotFoundError(self.filePath)
        with f:
            # books.csv에 객체들을 담을 빈 리스트
            # 생성자에 매개변수로 받게 되면 stateful 하게 되므로 데이터가 덮어 씌어질 수 있음
            # 그러므로 load_all 함수를 불러 올때마다 books 리스트 생성
            books = []

            # csv.reader는 각 줄을 리스트로 반환한다.
            reader = csv.reader(f)

            try:
                # 만약 첫 줄이 헤더 (제목,저자..와 같은 행)이라면 한 줄 건너뛴다.
                # 파일이 비어있을 경우 StopIteration 예외 발생
                next(reader)
            except StopIteration:
                return [] #빈 파일이면 빈 리스트 반환

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
        """
            메모리상의 도서 목록을 CSV 파일에 덮어쓰기 방식으로 저장한다.
            
            Argument:
                :param books: 저장할 book 객체 인스턴스들이 담긴 리스트
            Raises:
                :raise FileExtensionNotFound: 파일 확장자가 .csv 파일이 아닐 때
                :raise PermissionError: 엑셀 등 외부 프로그램 점유로 권한 오류 에러 처리
        """
        if not self.filePath.endswith(".csv"):
            raise FileExtensionNotFound(self.filePath)

        try:
            # "w" 모드 시 다른 프로그램 (엑셀 등)에 의해 열려있으면 PermissionError 발생
            f= open(self.filePath, "w", encoding="utf-8", newline='')
        except PermissionError:
            print(f"{self.filePath}가 다른 프로그램에서 사용중입니다. 닫고 다시 시작해주세요")
            return
        with f:
            writer = csv.writer(f)
            # [title],[author],[isbn] 헤더를 붙여 줌
            writer.writerow(["title", "author", "isbn"])

            for book in books:
                # 해당 컬럼에 열에 책에 제목 저자 isbn 추가
                writer.writerow([book.title, book.author, book.isbn])