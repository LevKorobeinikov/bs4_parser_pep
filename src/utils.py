import logging
from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException, PageLoadException

PAGE_LOAD_EXCEPTION = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding='utf-8'):
    """Перехват ошибки старницы"""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise PageLoadException(PAGE_LOAD_EXCEPTION.format(url=url))


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тэга"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_message = TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        logging.warning(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return searched_tag


def get_soup(session, url, features='lxml'):
    """Делаем суп"""
    response = get_response(session, url)
    return BeautifulSoup(response.text, features=features)


def get_results_dict(dictionary):
    results = {}
    for statuses in dictionary.values():
        for status in statuses:
            results[status] = 0
    return results
