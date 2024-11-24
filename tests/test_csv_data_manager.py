import pytest

from core.data_types import Book
from core.exceptions import IDErorr
from core.managers import CSVDataManager


def test_create_single_entry(csv_manager: CSVDataManager, book_model: Book):
    """Тест создания одной записи."""
    result = csv_manager.create(book_model)
    assert result['id'] == 1
    assert result['title'] == 'Test Book'
    assert result['author'] == 'Author 1'
    assert result['year'] == 2024
    assert result['status'] == 'В наличии'


def test_create_multiple_entries(csv_manager: CSVDataManager, book_models: list[Book]):
    """Тест создания нескольких записей."""
    results = csv_manager.create(book_models)
    assert len(results) == 2
    assert results[0]['id'] == 1
    assert results[0]['title'] == 'Book 1'
    assert results[0]['author'] == 'Author A'
    assert results[0]['year'] == 2024
    assert results[0]['status'] == 'В наличии'
    assert results[1]['id'] == 2
    assert results[1]['title'] == 'Book 2'
    assert results[1]['author'] == 'Author B'
    assert results[1]['year'] == 2024
    assert results[1]['status'] == 'В наличии'


def test_read_list(csv_manager: CSVDataManager, book_models: list[Book]):
    """Тест чтения всех записей."""
    csv_manager.create(book_models)
    result = csv_manager.read_list()
    assert len(result) == 2
    assert result[0]['id'] == '1'
    assert result[0]['title'] == 'Book 1'
    assert result[0]['author'] == 'Author A'
    assert result[0]['year'] == '2024'
    assert result[0]['status'] == 'В наличии'
    assert result[1]['id'] == '2'
    assert result[1]['title'] == 'Book 2'
    assert result[1]['author'] == 'Author B'
    assert result[1]['year'] == '2024'
    assert result[1]['status'] == 'В наличии'


def test_read_detail(csv_manager: CSVDataManager, book_model: Book):
    """Тест чтения одной записи по id."""
    csv_manager.create(book_model)
    result = csv_manager.read_detail(1)
    assert result['id'] == '1'
    assert result['title'] == 'Test Book'
    assert result['author'] == 'Author 1'
    assert result['year'] == '2024'
    assert result['status'] == 'В наличии'


def test_update_entry(csv_manager: CSVDataManager, book_model: Book):
    """Тест обновления записи."""
    csv_manager.create(book_model)
    updated_model = Book(title='Updated Book', author='Updated Author', year=2023)
    result = csv_manager.udate(1, updated_model)
    assert result['id'] == 1
    assert result['title'] == 'Updated Book'
    assert result['author'] == 'Updated Author'
    assert result['year'] == 2023
    assert result['status'] == 'В наличии'


def test_delete_entry(csv_manager: CSVDataManager, book_model: Book):
    """Тест удаления записи."""
    csv_manager.create(book_model)
    deleted = csv_manager.delete(1)
    assert deleted['id'] == '1'
    assert deleted['title'] == 'Test Book'
    assert deleted['author'] == 'Author 1'
    assert deleted['year'] == '2024'
    assert deleted['status'] == 'В наличии'
    assert len(csv_manager.read_list()) == 0


def test_search(csv_manager: CSVDataManager, book_models: list[Book]):
    """Тест поиска записей."""
    book_models.append(Book(title='Another Book', author='Author A', year=2024))
    csv_manager.create(book_models)
    results = csv_manager.search(field='author', value='Author A')
    assert len(results) == 2
    assert results[0]['title'] == 'Book 1'
    assert results[1]['title'] == 'Another Book'


def test_invalid_id_read(csv_manager: CSVDataManager):
    """Тест чтения несуществующей записи."""
    with pytest.raises(IDErorr, match='ID 1 не существует'):
        csv_manager.read_detail(1)


def test_invalid_field_search(csv_manager: CSVDataManager):
    """Тест поиска по неверному полю."""
    with pytest.raises(ValueError, match='Поля some_field нет в файле.'):
        csv_manager.search(field='some_field', value='Test')


def test_is_csv():
    """Тест проверки расширения файла."""
    with pytest.raises(ValueError, match='Файл data/test_data.txt не является CSV файлом.'):
        CSVDataManager(path='data/test_data.txt', fieldnames=['title', 'author'])
