from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BAD_LINK = 'Сбой при переходе по ссылке: {link}'
LINKS_LOG = '{data}'
PARSER_START = 'Парсер запущен!'
ARGUMENTS = 'Аргументы командной строки: {args}'
PARSER_COMPLETE = 'Парсер завершил работу.'
RESULTS_SAVE = 'Файл с результатами был сохранён: {file_path}'
ERROR_LOG = ('Ошибка во время работы парсера. {error}')
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
LINK_TITLE_EDITOR_AUTHOR = ('Ссылка на статью', 'Заголовок', 'Редактор, автор')
LINK_VERSION_STATUS = ('Ссылка на документацию', 'Версия', 'Статус')
STATUS_COUNT = ['Статус', 'Количество']
