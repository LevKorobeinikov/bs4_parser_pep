import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    DATETIME_FORMAT, RESULTS_SAVE, RESULTA_DIR,
    STATUS_COUNT, PRETTY, FILE
)


def control_output(results, cli_args):
    """Определяет метод вывода результатов."""
    output_handlers = {
        PRETTY: pretty_output,
        FILE: file_output,
        None: default_output
    }
    output_handler = output_handlers.get(cli_args.output, default_output)
    output_handler(results, cli_args)


def default_output(results):
    if isinstance(results, dict):
        for key, value in results.items():
            print(f'{key}: {value}')
    else:
        for row in results:
            print(*row)


def pretty_output(results, cli_args=None):
    table = PrettyTable()
    if isinstance(results, dict):
        table.field_names = list(results.keys())
        table.add_row(list(results.values()))
    else:
        table.field_names = results[0]
        table.align = 'l'
        table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = RESULTA_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect=csv.excel)
        if isinstance(results, dict):
            writer.writerow(STATUS_COUNT)
            writer.writerows(results.items())
        else:
            writer.writerows(results)
    logging.info(RESULTS_SAVE.format(file_path=file_path))
