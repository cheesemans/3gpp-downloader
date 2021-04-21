# Python program to download 3gpp documents

# Imports
import requests, zipfile, io
import pandas as pd

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

def build_specification_link():
    specification_version_table = pd.DataFrame([])
    print(specification_version_table.empty)
    while specification_version_table.empty:
        specification_archive_url = get_specification_archive_url()
        specification_version_table = get_specification_versions(specification_archive_url)
    url = select_version(specification_version_table)
    return url


def get_specification_archive_url():
    spec = input('Specification number: ')
    # spec = '38.413'
    series = spec.partition('.')[0]
    return f'https://www.3gpp.org/ftp/Specs/archive/{series}_series/{spec}'


def get_specification_versions(url):
    parsed_table = pd.DataFrame([])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table')
        if len(tables) > 1:
            print('Make script handle pages with multiple tables')
        else:
            parsed_table = parse_html_table(tables[0])
    finally:
        return parsed_table


def select_version(specification_table):
    table_array = specification_table.to_numpy()
    option_iterator = 0
    print('%-5s' % 'Nr', '%-15s' % 'Version', '%s' % 'Release date')
    for row in table_array:
        print('%-5s' % (str(option_iterator) + ':'), '%-15s' % row[1], '%s' % row [2])
        option_iterator += 1
    choice = int(input(f'Choose a version to download (from 0 - {option_iterator-1}): '))
    url = table_array[choice][0]
    return url


def parse_html_table(html_table):
    n_columns, n_rows = get_nr_rows_cols(html_table)

    parsed_table = extract_table_data(html_table, n_columns, n_rows)

    return parsed_table


def get_nr_rows_cols(html_table):
    n_columns = 0
    n_rows = 0

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in html_table.find_all('tr'):

        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows += 1
            if n_columns == 0:
                # Set the number of columns for the table
                n_columns = len(td_tags)

    return {n_columns, n_rows}


def extract_table_data(html_table, n_columns, n_rows):
    table = pd.DataFrame(columns = range(0, n_columns), index = range(0, n_rows))

    row_marker = 0
    for row in html_table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            column_text = []

            if column.a != None:
                table.iat[row_marker, column_marker - 1]  = column.a['href']

            column_text = column.get_text()
            table.iat[row_marker, column_marker] = column_text.strip().strip('.zip')
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    return table


def download_url(url, save_path='downloads'):
    r = requests.get(url, stream = True)
    if r.ok:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(save_path)


def main():
    download_link = build_specification_link()
    download_url(download_link)


if __name__ == '__main__':
    main()
