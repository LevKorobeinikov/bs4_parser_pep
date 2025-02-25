from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

PAGE_LOAD_EXCEPTION = 'Возникла ошибка при загрузке страницы {url} - {error}'
TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    """Перехват ошибки старницы"""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(PAGE_LOAD_EXCEPTION.format(url=url, error=error))


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тэга"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_message = TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        raise ParserFindTagException(error_message)
    return searched_tag


def get_soup(session, url, features='lxml'):
    """Делаем суп"""
    return BeautifulSoup(get_response(session, url).text, features=features)
