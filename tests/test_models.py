from datetime import datetime

import pytest

from core.data_types import Book, Status


def test_valid_book():
    """Тест на корректное создание экземпляра книги с валидными данными."""
    book = Book(title='Название книги', author='Автор', year=2023, status='В наличии')
    assert book.title == 'Название книги'
    assert book.author == 'Автор'
    assert book.year == 2023
    assert book.status == 'В наличии'


@pytest.mark.parametrize('title', ['', '   '])
def test_invalid_title(title: str | int):
    """Тест на валидацию поля title."""
    with pytest.raises(ValueError, match='Поле `Название` должно быть непустой строкой.'):
        Book(title=title, author='Автор', year=2023, status='В наличии')


@pytest.mark.parametrize('author', ['', '   '])
def test_invalid_author(author: str | int):
    """Тест на валидацию поля author."""
    with pytest.raises(ValueError, match='Поле `Автор` должно быть непустой строкой.'):
        Book(title='Название книги', author=author, year=2023, status='В наличии')


@pytest.mark.parametrize(
    'year',
    ['abcd', -1, 3000],
)
def test_invalid_year(year: str | int):
    """Тест на валидацию поля year."""
    current_year = datetime.now().year
    expected_error = f'Поле `Год издания` должно быть целым числом в диапазоне 0-{current_year}.'
    with pytest.raises(ValueError, match=expected_error):
        Book(title='Название книги', author='Автор', year=year, status='В наличии')


@pytest.mark.parametrize(
    'status',
    ['Неизвестный статус', 123, ''],
)
def test_invalid_status(status: str | int):
    """Тест на валидацию поля status."""
    with pytest.raises(ValueError, match='Поле `status` должно быть одним из значений:'):
        Book(title='Название книги', author='Автор', year=2023, status=status)


def test_default_status():
    """Тест на значение поля status по умолчанию."""
    book = Book(title='Название книги', author='Автор', year=2023)
    assert book.status == Status.IN_STOCK.value
