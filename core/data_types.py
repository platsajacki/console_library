from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum

ModelDict = dict


@dataclass
class Model:
    """Базовая модель."""

    @classmethod
    def get_fields(cls) -> list[str]:
        return list(cls.__annotations__.keys())

    def to_dict(self) -> ModelDict:
        return asdict(self)


class Status(Enum):
    IN_STOCK = 'В наличии'
    GIVEN = 'Выдана'


@dataclass
class Book(Model):
    """Модель описывающая книгу."""

    title: str
    author: str
    year: int | str
    status: str = Status.IN_STOCK.value

    def __post_init__(self):
        self.validate_fields()

    def validate_fields(self):
        self.validate_title()
        self.validate_author()
        self.validate_year()
        self.validate_status()

    def validate_title(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError(f'Поле `title` должно быть непустой строкой.\nПолучено: {self.title}')

    def validate_author(self):
        if not isinstance(self.author, str) or not self.author.strip():
            raise ValueError(f'Поле `author` должно быть непустой строкой.\nПолучено: {self.author}')

    def validate_year(self):
        year = datetime.now().year
        error = ValueError(f'Поле `year` должно быть целым числом в диапазоне 0-{year}.\nПолучено: {self.year}')
        if not self.year.isdigit():
            raise error
        self.year = int(self.year)
        if self.year < 0 or self.year > year:
            raise error

    def validate_status(self):
        try:
            self.status = Status(self.status).value
        except ValueError:
            raise ValueError(
                f'Поле `status` должно быть одним из значений: {[status.value for status in Status]}.'
                f'\nПолучено: {self.status}'
            )


class TextFormat(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
