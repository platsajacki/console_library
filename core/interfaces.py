import sys
from abc import ABC, abstractmethod
from typing import Any, Sequence

from core.constants import GOOD_BAY
from core.data_types import Model, TextFormat


class BaseService(ABC):
    """
    Базовый класс для создания сервисов с единообразным интерфейсом.

    Этот класс используется в качестве шаблона для реализации сервисов, которые
    выполняют определённое действие при вызове экземпляра. Он определяет
    абстрактный метод `act`, который должен быть реализован в подклассах.

    Пример использования:
        class MyService(BaseService):
            def act(self) -> str:
                return "Выполнение сервиса"

        service = MyService()
        result = service()  # Эквивалентно вызову service.act()
        print(result)  # Выведет: "Выполнение сервиса"
    """

    def __call__(self) -> Any:
        """
        Вызывает метод act() при вызове экземпляра класса.

        Возвращает:
            Любой результат, возвращённый методом act().
        """
        return self.act()

    @abstractmethod
    def act(self) -> Any:
        """
        Абстрактный метод, который должен быть реализован в подклассе.

        Этот метод содержит основную логику сервиса, которая будет
        выполняться при вызове экземпляра.

        Возвращает:
            Результат выполнения сервиса (любой тип данных).
        """
        return NotImplemented


class ConsoleService(BaseService):
    """Сервис для работы с выводом данных в консоль."""

    def _get_fmt_text(self, data: str, text_format: TextFormat, bold: bool):
        return f'{TextFormat.BOLD.value if bold else ''}{text_format.value}{data}{TextFormat.RESET.value}'

    def write(self, data: str, text_format: TextFormat = TextFormat.RESET, bold: bool = True) -> None:
        """Выводит данные в консоль с указанным цветом."""
        text = self._get_fmt_text(data, text_format, bold)
        print(text)

    def input(self, data: str, text_format: TextFormat = TextFormat.RESET, bold: bool = True) -> str:
        """Выводит данные в консоль с указанным цветом."""
        try:
            text = self._get_fmt_text(data, text_format, bold)
            return input(text).strip()
        except KeyboardInterrupt:
            self.write(GOOD_BAY, TextFormat.GREEN)
            sys.exit(0)


class DataManager(ABC):
    """
    Определяет интерфейс для выполнения CRUD-операций.
    Каждая реализация должна предоставить конкретные методы для работы с данными.
    """

    @abstractmethod
    def create(self, data: Model | Sequence[Model]) -> Any:  # type: ignore
        """Создает новую запись или записи в источнике данных."""
        return NotImplemented

    @abstractmethod
    def read_list(self) -> Any:
        """Читает и возвращает список записей из источника данных."""
        return NotImplemented

    @abstractmethod
    def read_detail(self, id: int) -> Any:
        """Читает и возвращает одну запись из источника данных."""
        return NotImplemented

    @abstractmethod
    def udate(self, id: int, data: Model) -> Any:
        """Обновляет существующую запись в источнике данных."""
        return NotImplemented

    @abstractmethod
    def delete(self, id: int) -> Any:
        """Удаляет запись из источника данных."""
        return NotImplemented

    @abstractmethod
    def search(self, field: str, value: str) -> Any:
        """Ищет объекты по отпределенному полю."""
        return NotImplemented
