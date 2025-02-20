import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESULTS_SAVE, STATUS_COUNT


def control_output(results, cli_args):
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    if isinstance(results, dict):
        for key, value in results.items():
            print(f'{key}: {value}')
    else:
        for row in results:
            print(*row)


def pretty_output(results):
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
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        if isinstance(results, dict):
            writer.writerow(STATUS_COUNT)
            for key, value in results.items():
                writer.writerow([key, value])
        else:
            writer.writerows(results)
    logging.info(RESULTS_SAVE.format(file_path=file_path))
