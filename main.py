from core.console import BookConsoleService
from core.data_types import Book
from core.managers import CSVDataManager

book_manager = CSVDataManager('data/db.csv', Book.get_fields())

BookConsoleService(book_manager)()
