import csv
import os
import sys
import re
from bs4 import BeautifulSoup
from eventlet import GreenPool
from eventlet.green.urllib.request import urlopen

base = 'http://en.wikipedia.org'
ref_pattern = r'\[.+?\]'
pool = GreenPool()
data = {
    'links': [],
    'titles': [],
    'sites': [],
    'genres': [],
    'demographics': [],
    'numepisodes': [],
    'descriptions': []
}


def get_soup(url):
    with urlopen(url) as resp:
        data = resp.read()
    return BeautifulSoup(data, 'lxml')


def scrape_page(item):
    page_data = {}
    page_data['title'] = item.find('i').text
    anchors = item.select('a')
    if len(anchors) > 1:
        sitesanchors = anchors[1:]
        path = anchors[0].get('href')
        tempsoup = get_soup(base + path)
        print('...')
    else:
        sitesanchors = [anchors[0]]
        tempsoup = None
    page_data['site'] = ', '.join([siteanchor.text for siteanchor in sitesanchors])
    try:
        genrecell = tempsoup.find('th', text='Genre')
        genredata = re.sub(ref_pattern, '', genrecell.find_next('td').text.replace('\n', ', '))
    except AttributeError:
        genredata = 'n/a'
    page_data['genre'] = genredata
    try:
        demographiccell = tempsoup.find('th', text='Demographic')
        demographicdata = demographiccell.find_next('td').text.split()[0]
    except (AttributeError, IndexError):
        demographicdata = 'n/a'
    page_data['demographic'] = demographicdata
    try:
        episodescell = tempsoup.find('th', text='Episodes')
        episodesdata = int(episodescell.find_next('td').text.split()[0])
    except (AttributeError, IndexError, ValueError):
        episodesdata = 0
    page_data['numepisodes'] = episodesdata
    try:
        description = re.sub(ref_pattern, '', tempsoup.select_one('div#mw-content-text > p').text)
    except AttributeError:
        description = 'n/a'
    page_data['description'] = description
    return page_data


def get_data(url, header):
    soup = get_soup(url)
    seasonheader = soup.select_one('span#%s' % header)
    section = seasonheader.find_next('ul')
    items = section.select('li')
    results = pool.imap(scrape_page, items)
    for result in results:
        for key in ('title', 'site', 'genre', 'demographic', 'numepisodes', 'description'):
            data_key = key + 's' if not key.endswith('s') else key
            data[data_key].append(result[key])


def export_csv(output, newfile):
    with open('output/' + newfile, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(('Title', 'Sites', 'Genres', 'Demographic', 'Episodes', 'Description'))
        csv_writer.writerows(output)
# Excel: Data, From Text, Unicode (UTF-8), Comma


def export_sql_and_html(csv_file, season):
    html_file = 'wiki_simulcasts_%s.html' % season
    table_name = 'w_%s' % season
    os.chdir('output')
    with open('sqlite_script.sql', 'w') as f:
        f.write('\n'.join((
            '.mode csv',
            'BEGIN TRANSACTION;',
            'DROP TABLE IF EXISTS %s;' % table_name,
            '.import %s temp_table' % (csv_file),
            'CREATE TABLE %s (Title TEXT, Sites TEXT, Genres TEXT, Demographic TEXT, Episodes INTEGER, Description TEXT);' % table_name,
            'INSERT INTO %s SELECT * FROM temp_table;' % table_name,
            'DROP TABLE temp_table;',
            'COMMIT;',
            '.headers on',
            '.mode html',
            '.once %s' % html_file,
            'SELECT * from %s;' % table_name
        )))
    os.system('sqlite3 data.db < sqlite_script.sql')
    os.remove('sqlite_script.sql')
    with open(html_file, encoding='utf-8') as f:
        contents = f.read()
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join((
            '<meta charset="utf-8">',
            '<style>table td { border: 1px solid black; } table { border-collapse: collapse; }</style>',
            '<table>',
            contents,
            '</table>'
        )))
    os.chdir('..')


def main(season, test_sql=False):
    url = 'http://en.wikipedia.org/wiki/List_of_US_anime_simulcasts'
    csv_file = 'wiki_simulcasts_%s.csv' % season
    if not test_sql:
        get_data(url, season)
        print('Saving...\n')
        zipped = tuple(zip(data['titles'], data['sites'], data['genres'],
                           data['demographics'], data['numepisodes'], data['descriptions']))
        export_csv(zipped, csv_file)
    export_sql_and_html(csv_file, season)


if __name__ == '__main__':
    usage = 'Usage: python wiki_simulcasts.py [season uppercase]_[year]'
    try:
        season = sys.argv[1]
        test_sql = True if len(sys.argv) > 2 and sys.argv[2] == '-t' else False
    except IndexError:
        sys.exit(usage)
    if '_' not in season:
        sys.exit(usage)
    main(season, test_sql)
