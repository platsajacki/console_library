from dataclasses import dataclass

from core.constants import (
    BOOK_ADD,
    BOOK_AUTHOR,
    BOOK_TITLE,
    BOOK_YEAR,
    ERORR_CHOISE,
    ERORR_YEAR,
    GREETING,
    MENU,
    MENU_BUTTON,
)
from core.data_types import Book, TextFormat
from core.interfaces import ConsoleService
from core.managers import CSVDataManager


@dataclass
class BookConsoleService(ConsoleService):
    manager: CSVDataManager

    def is_correct_intenger(self, value: str, text: str) -> bool:
        """Проверяет, что введен правильный вариант ответа int."""
        return value in text and value.isdigit()

    def handle_menu(self) -> None | str:
        self.write(MENU, TextFormat.BLUE)
        text = self.input(MENU_BUTTON, TextFormat.YELLOW)
        if not self.is_correct_intenger(text, MENU):
            self.write(ERORR_CHOISE, TextFormat.RED)
            return None
        return text

    def handle_action(self, menu: str) -> None:
        match menu:
            case '1':
                self.add_book()

    def add_book(self) -> None:
        title = self.input(BOOK_TITLE, TextFormat.BLUE)
        author = self.input(BOOK_AUTHOR, TextFormat.BLUE)
        year = self.input(BOOK_YEAR, TextFormat.BLUE)
        if not year.isdigit():
            self.write(ERORR_YEAR, TextFormat.RED)
            return
        book = Book(title=title, author=author, year=int(year))
        book_dict = self.manager.create(book)
        self.write(BOOK_ADD.format(**book_dict), TextFormat.GREEN)

    def act(self) -> None:
        self.write(GREETING, TextFormat.GREEN)
        while True:
            menu = self.handle_menu()
            if not menu:
                continue
            self.handle_action(menu)
