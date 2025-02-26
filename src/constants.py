from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS = 'results'
DOWNLOADS = 'downloads'
RESULTS_DIR = BASE_DIR / RESULTS
DOWNLOADS_DIR = BASE_DIR / DOWNLOADS

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

BAD_LINK = 'Сбой при переходе по ссылке: {link}: {error}'
LINKS_LOG = '{data}'
PARSER_START = 'Парсер запущен!'
ARGUMENTS = 'Аргументы командной строки: {args}'
PARSER_COMPLETE = 'Парсер завершил работу.'
RESULTS_SAVE = 'Файл с результатами был сохранён: {file_path}'
NOT_FOUND = 'Ничего не нашлось'
DOWNLOADS_COMPLETE = 'Архив был загружен и сохранён: {archive_path}'
ERROR_LOG = 'Исключение во время работы парсера. {error}'
PARSER_ERROR = 'Ошибка парсера.'
UNKNOWN_MODE = 'Неизвестный режим: {args}'

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

PRETTY = 'pretty'
FILE = 'file'
