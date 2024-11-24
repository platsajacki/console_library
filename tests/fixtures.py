import os

import pytest

from core.console import BookConsoleService
from core.data_types import Book
from core.managers import CSVDataManager


@pytest.fixture
def csv_manager():
    """Фикстура для создания CSVDataManager с тестовыми данными."""
    TEST_CSV_FILE = 'data/test_data.csv'
    manager = CSVDataManager(path=TEST_CSV_FILE, fieldnames=Book.get_fields())
    yield manager
    if os.path.exists(TEST_CSV_FILE):
        os.remove(TEST_CSV_FILE)


@pytest.fixture
def book_model() -> Book:
    """Возвращает модель книги."""
    return Book(title='Test Book', author='Author 1', year=2024)


@pytest.fixture
def book_models() -> list[Book]:
    """Возвращает модели книг."""
    return [
        Book(title='Book 1', author='Author A', year=2024),
        Book(title='Book 2', author='Author B', year=2024),
    ]


@pytest.fixture
def console(csv_manager: CSVDataManager) -> BookConsoleService:
    return BookConsoleService(csv_manager)
