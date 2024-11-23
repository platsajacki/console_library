GOOD_BAY = '\n\nДо скорой встречи!'

GREETING = 'Добро пожаловать в "Консольную Библиотеку"\n'

MENU = '''1. Добавление книги
2. Отображение книг
3. Поиск книги
4. Изменение статуса книги
5. Обновление книги
6. Удаление книги
'''
MENU_GET_BOOK = '''
1. Показать всю библиотеку
2. Найти книгу по ID
'''
SEARCH_DICT = {'1': ('title', 'Название'), '2': ('author', 'Автор'), '3': ('year', 'Год издания')}
MENU_SEARCH_BOOK = f'''
Найти книгу по:
1. {SEARCH_DICT['1'][1]}
2. {SEARCH_DICT['2'][1]}
3. {SEARCH_DICT['3'][1]}
'''

MENU_BUTTON = 'Введите номер пункта меню: '

ERORR_CHOISE = '\nНеверно выбран пункт меню.\n'
ERORR_YEAR = '\nГод должен быть положительным числом.\n'

BOOK_INPUT = '\nВведите {} книги: '
BOOK_ID = BOOK_INPUT.format('ID')
BOOK_TITLE = BOOK_INPUT.format('название')
BOOK_AUTHOR = BOOK_INPUT.format('автора')
BOOK_YEAR = BOOK_INPUT.format('год издания')
BOOK_STATUS = BOOK_INPUT.format('статус')
BOOK = '''
ID - `{id}`
Название - `{title}`
Aвтор - `{author}`
Год издания - `{year}`
Статус - `{status}`
'''
BOOK_ADD = (
    '''
Добавлена книга:
'''
    + BOOK
)
BOOK_GET = (
    '''
Найдена книга:
'''
    + BOOK
)
BOOK_LIST = '''| {id} | {title} | {author} | {year} | {status} |'''
