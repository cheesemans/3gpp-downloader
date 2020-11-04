# Python program to download 3gpp documents

# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

def build_specification_link():
    specification_archive_url = get_specification_archive_url()
    specification_version_table = get_specification_versions(specification_archive_url)
    download_link = select_version(specification_version_table)
    print(download_link)

def select_version(specification_table):
    table_array = specification_table.to_numpy()
    option_iterator = 0
    print('%-5s' % "Nr", '%-15s' % "Version", '%s' % "Release date")
    for row in table_array:
        option_iterator += 1
        print('%-5s' % (str(option_iterator) + ":"), '%-15s' % row[1], '%s' % row [2])
    choice = int(input("Choose a version to download (from 1 - %i): " % option_iterator))
    return table_array[choice - 1][0]

def get_specification_archive_url():
    #spec = input("Specification number: ")
    spec = "38.413"
    series = spec.partition(".")[0]
    return "https://www.3gpp.org/ftp/Specs/archive/" + series + "_series/" + spec

def get_specification_versions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table')
    if len(tables) > 1:
        print("Make script handle pages with multiple tables")
    else:
        return parse_html_table(tables[0])

def parse_html_table(html_table):
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

    parsed_table = pd.DataFrame(columns = range(0, n_columns), index = range(0, n_rows))

    row_marker = 0
    for row in html_table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            column_text = []

            if column.a != None:
                parsed_table.iat[row_marker, column_marker - 1]  = column.a['href']

            column_text = column.get_text()
            parsed_table.iat[row_marker, column_marker] = column_text.strip().strip('.zip')
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    return parsed_table

def main():
    download_link = build_specification_link()

if __name__ == "__main__":
    main()
