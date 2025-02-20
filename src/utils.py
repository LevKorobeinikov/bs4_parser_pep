import logging
from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    """Перехват ошибки старницы"""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тэга"""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.warning(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url):
    """Делаем суп"""
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def get_results_dict(dictionary):
    results = {}
    for statuses in dictionary.values():
        for status in statuses:
            results[status] = 0
    return results
