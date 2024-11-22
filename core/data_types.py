from dataclasses import dataclass, asdict
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
    year: int
    status: Status = Status.IN_STOCK

    def __post_init__(self):
        self.status = self.status.value


class TextFormat(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
