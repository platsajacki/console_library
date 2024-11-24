from copy import deepcopy
from unittest.mock import Mock

import pytest

from core.console import BookConsoleService
from core.constants import BOOK_ADD, BOOK_DELETE, BOOK_GET, BOOK_UPDATE, ERORR_CHOISE, MENU
from core.data_types import Book, Status, TextFormat
from core.managers import CSVDataManager


def test_is_correct_menu_intenger_valide(console: BookConsoleService):
    """Проверяет корректную обработку допустимого значения меню."""
    assert console.is_correct_menu_intenger('1', MENU) is True


@pytest.mark.parametrize('value', ['test', '212', ' '])
def test_is_correct_menu_intenger_invalide(console: BookConsoleService, value: str):
    """Проверяет обработку недопустимых значений меню."""
    assert console.is_correct_menu_intenger(value, MENU) is False


def test_get_intenger_valide(console: BookConsoleService):
    """Проверяет преобразование корректного целого числа."""
    value = console.get_intenger('1')
    assert value == 1


def test_get_intenger_invalide(console: BookConsoleService):
    """Проверяет вызов исключения при некорректном вводе целого числа."""
    with pytest.raises(ValueError):
        value = console.get_intenger('test')
        assert value == 1


def test_handle_menu_valid(console: BookConsoleService):
    """Проверяет обработку корректного выбора пункта меню."""
    console.input = Mock(return_value='1')  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    result = console.handle_menu(MENU)
    assert result == '1'


def test_handle_menu_invalid(console: BookConsoleService):
    """Проверяет обработку некорректного выбора пункта меню."""
    console.input = Mock(return_value='invalid')  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    result = console.handle_menu(MENU)
    assert result is None
    console.write.assert_called_with(ERORR_CHOISE, TextFormat.RED)


def test_add_book_valid(console: BookConsoleService, csv_manager: CSVDataManager, book_model: Book):
    """Проверяет добавление книги с корректными данными."""
    console.input = Mock(side_effect=['New Book', 'Author X', '2023'])  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    model_dict = {'id': 1} | book_model.to_dict()
    csv_manager.create = Mock(return_value=model_dict)  # type: ignore[method-assign]
    console.add_book()
    console.write.assert_called_with(BOOK_ADD.format(**model_dict), TextFormat.GREEN)


def test_add_book_invalid_year(console: BookConsoleService):
    """Проверяет вызов исключения при некорректном вводе года публикации."""
    console.input = Mock(side_effect=['New Book', 'Author X', 'invalid'])  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    with pytest.raises(ValueError):
        console.add_book()
    console.write.assert_not_called()


def test_get_list_empty(console: BookConsoleService, csv_manager: CSVDataManager):
    """Проверяет вывод сообщения при отсутствии записей."""
    csv_manager.read_list = Mock(return_value=[])  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    console.get_list()
    console.write.assert_called_with('\nПо вашему запросу ничего не найдено.', TextFormat.YELLOW)


def test_get_list_with_data(console: BookConsoleService, csv_manager: CSVDataManager, book_model: Book):
    """Проверяет корректный вывод списка книг."""
    model_dict = {'id': 1} | book_model.to_dict()
    csv_manager.read_list = Mock(return_value=[model_dict, model_dict, model_dict])  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    console.get_list()
    assert console.write.call_count == 5


def test_request_id_valid(console: BookConsoleService):
    """Проверяет корректный ввод идентификатора."""
    console.input = Mock(return_value='123')  # type: ignore[method-assign]
    result = console.request_id()
    assert result == 123


def test_request_id_invalid(console: BookConsoleService):
    """Проверяет вызов исключения при некорректном идентификаторе."""
    console.input = Mock(return_value='invalid')  # type: ignore[method-assign]
    with pytest.raises(ValueError):
        console.request_id()


def test_get_detail_valid(console: BookConsoleService, csv_manager: CSVDataManager, book_model: Book):
    """Проверяет вывод детальной информации о книге."""
    model_dict = {'id': 1} | book_model.to_dict()
    csv_manager.read_detail = Mock(return_value=model_dict)  # type: ignore[method-assign]
    console.input = Mock(return_value='1')  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    console.get_detail()
    console.write.assert_called_with(BOOK_GET.format(**model_dict), TextFormat.GREEN)


def test_change_status_valid(console: BookConsoleService, csv_manager: CSVDataManager, book_model: Book):
    """Проверяет изменение статуса книги."""
    model_dict = {'id': 1} | book_model.to_dict()
    csv_manager.read_detail = Mock(return_value=model_dict)  # type: ignore[method-assign]
    update_data = deepcopy(model_dict)
    update_data['status'] = Status.GIVEN.value
    csv_manager.udate = Mock(return_value=update_data)  # type: ignore[method-assign]
    console.input = Mock(side_effect=['1', '2'])  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    console.change_status()
    console.write.assert_called_with(BOOK_UPDATE.format(**update_data), TextFormat.GREEN)


def test_delete_book_valid(console: BookConsoleService, csv_manager: CSVDataManager, book_model: Book):
    """Проверяет удаление книги с корректным идентификатором."""
    model_dict = {'id': 1} | book_model.to_dict()
    csv_manager.delete = Mock(return_value=model_dict)  # type: ignore[method-assign]
    console.input = Mock(return_value='1')  # type: ignore[method-assign]
    console.write = Mock()  # type: ignore[method-assign]
    console.delete_book()
    console.write.assert_called_with(BOOK_DELETE.format(**model_dict), TextFormat.GREEN)
