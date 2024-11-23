from dataclasses import dataclass

from core.constants import (
    BOOK_ADD,
    BOOK_AUTHOR,
    BOOK_GET,
    BOOK_ID,
    BOOK_INPUT,
    BOOK_LIST,
    BOOK_TITLE,
    BOOK_YEAR,
    ERORR_CHOISE,
    ERORR_YEAR,
    GREETING,
    MENU,
    MENU_BUTTON,
    MENU_GET_BOOK,
    MENU_SEARCH_BOOK,
    SEARCH_DICT,
)
from core.data_types import Book, ModelDict, TextFormat
from core.exceptions import IDErorr
from core.interfaces import ConsoleService
from core.managers import CSVDataManager


@dataclass
class BookConsoleService(ConsoleService):
    manager: CSVDataManager

    def is_correct_menu_intenger(self, value: str, text: str) -> bool:
        """Проверяет, что введен правильный вариант ответа int."""
        return value in text and value.isdigit()

    def get_intenger(self, value: str) -> int:
        """Возвращает число, если это возможно."""
        if value.isdigit():
            return int(value)
        raise ValueError('ID должно быть числом.')

    def handle_menu(self, menu: str) -> None | str:
        """Обработчик главного меню."""
        self.write(menu, TextFormat.BLUE)
        text = self.input(MENU_BUTTON, TextFormat.YELLOW)
        if not self.is_correct_menu_intenger(text, menu):
            self.write(ERORR_CHOISE, TextFormat.RED)
            return None
        return text

    def handle_get_book_menu(self) -> None:
        """Обработчик меню получения книг."""
        match self.handle_menu(MENU_GET_BOOK):
            case '1':
                self.get_list()
            case '2':
                self.get_detail()

    def handle_action(self, menu: str) -> None:
        match menu:
            case '1':
                self.add_book()
            case '2':
                self.handle_get_book_menu()
            case '3':
                self.search_book()

    def add_book(self) -> None:
        title = self.input(BOOK_TITLE, TextFormat.BLUE)
        author = self.input(BOOK_AUTHOR, TextFormat.BLUE)
        year = self.input(BOOK_YEAR, TextFormat.BLUE)
        if not year.isdigit():
            self.write(ERORR_YEAR, TextFormat.RED)
            return
        book = Book(title=title, author=author, year=int(year))
        book_dict = self.manager.create(book)
        if isinstance(book_dict, list):
            raise ValueError('Внутренняя ошибка, попробуйте позже.')
        self.write(BOOK_ADD.format(**book_dict), TextFormat.GREEN)

    def show_list(self, book_dicts: list[ModelDict]) -> None:
        self.write('\nКниги:', TextFormat.GREEN)
        for book_dict in book_dicts:
            self.write(BOOK_LIST.format(**book_dict), TextFormat.GREEN)
        self.write('\n')

    def get_list(self) -> None:
        book_dicts = self.manager.read_list()
        self.show_list(book_dicts)

    def get_detail(self) -> None:
        str_id = self.input(BOOK_ID, TextFormat.BLUE)
        int_id = self.get_intenger(str_id)
        book_dict = self.manager.read_detail(int_id)
        self.write(BOOK_GET.format(**book_dict), TextFormat.GREEN)

    def search_book(self) -> None:
        text = self.handle_menu(MENU_SEARCH_BOOK)
        if not text:
            return
        field = SEARCH_DICT[text][0]
        value = self.input(BOOK_INPUT.format(SEARCH_DICT[text][1].lower()), TextFormat.BLUE)
        book_dicts = self.manager.search(field, value)
        self.show_list(book_dicts)

    def act(self) -> None:
        self.write(GREETING, TextFormat.GREEN)
        while True:
            menu = self.handle_menu(MENU)
            if not menu:
                continue
            try:
                self.handle_action(menu)
            except (ValueError, IDErorr) as e:
                self.write('\n%s\n' % str(e), TextFormat.RED)