import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from constants import (
    ARGUMENTS, BAD_LINK, BASE_DIR, ERROR_LOG, EXPECTED_STATUS,
    LINKS_LOG, LINK_TITLE_EDITOR_AUTHOR, LINK_VERSION_STATUS,
    MAIN_DOC_URL, MAIN_PEP_URL, PARSER_COMPLETE, PARSER_START
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import find_tag, get_soup, get_results_dict


NOT_FOUND = 'Ничего не нашлось'
DOWNLOADS_COMPLETE = 'Архив был загружен и сохранён: {archive_path}'


def whats_new(session):
    """Парсер о нововведениях в Python."""
    results = [LINK_TITLE_EDITOR_AUTHOR]
    unavailable_links = []
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        try:
            soup = get_soup(session, version_link)
        except ConnectionError:
            unavailable_links.append(
                BAD_LINK.format(
                    link=version_link
                )
            )
            continue
        results.append(
            (
                version_link, find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            )
        )
    if unavailable_links:
        logging.info(LINKS_LOG.format(data=unavailable_links))
    return results


def latest_versions(session):
    """Парсер статусов версий."""
    results = [LINK_VERSION_STATUS]
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception(NOT_FOUND)
    for a_tag in a_tags:
        text_match = re.search(
            r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)', a_tag.text
        )
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return results


def download(session):
    """Парсер, который скачивает архив документации."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table = main_tag.find('table')
    pdf_a4_tag = table.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOADS_COMPLETE.format(archive_path=archive_path))


def get_main_status_from_soup(soup, preview_status, url):
    """Извлекает статусы из страницы документа PEP для парсера."""
    for tag in soup.find('dl').find_all('dt'):
        if tag.text == 'Status:':
            main_status = tag.find_next_sibling().text.strip()
            if main_status not in EXPECTED_STATUS[preview_status]:
                logging.info(
                    f'Несовпадающие статусы: {url}\n'
                    f'Статус в карточке: {main_status}\n'
                    'Ожидаемые статусы:'
                    f'{EXPECTED_STATUS[preview_status]}'
                )
                return None
            return main_status
    return None


def pep(session):
    """Парсер документов PEP."""
    results = get_results_dict(EXPECTED_STATUS)
    soup = get_soup(session, MAIN_PEP_URL)
    table_bodies = [
        body for table in soup.find_all(
            'table', class_='pep-zero-table docutils align-default'
        )
        for body in table.find_all('tbody')
    ]
    for body in table_bodies:
        for row in tqdm(body.find_all('tr')):
            status_tag = find_tag(row, 'td')
            preview_status = status_tag.text[1:] if len(
                status_tag.text
            ) > 1 else ''
            link_tag = status_tag.find_next_sibling()
            url = urljoin(MAIN_PEP_URL, link_tag.find('a')['href'])
            soup = get_soup(session, url)
            main_status = get_main_status_from_soup(soup, preview_status, url)
            if main_status:
                results[main_status] += 1
    results['Total'] = sum(results.values())
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    try:
        configure_logging()
        logging.info(PARSER_START)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(ARGUMENTS.format(args=args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        results = MODE_TO_FUNCTION[args.mode](session)
        if results is not None:
            control_output(results, args)
        logging.info(PARSER_COMPLETE)
    except Exception as error:
        logging.exception(ERROR_LOG.format(error=error),)


if __name__ == '__main__':
    main()
