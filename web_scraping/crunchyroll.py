import csv
import os
import sys
from bs4 import BeautifulSoup
from eventlet import GreenPool
from eventlet.green.urllib.request import urlopen

base = 'http://www.crunchyroll.com'
pool = GreenPool()
data = {
    'titles': [],
    'descriptions': [],
    'ratings': [],
    'popularity': [],
    'numvideos': []
}


def get_soup(url):
    with urlopen(url) as resp:
        data = resp.read()
    return BeautifulSoup(data, 'lxml')


def scrape_page(link):
    page_data = {}
    page_data['title'] = link.get('title')
    path = link.get('href')
    page_data['numvideos'] = link.select('span')[2].text.strip().replace(' Videos', '')
    tempsoup = get_soup(base + path)
    print('...')
    try:
        description = tempsoup.select_one('meta[property=og:description]').get('content')
        page_data['description'] = ' '.join(description.split())
        page_data['rating'] = float(tempsoup.select_one('span[itemprop=ratingValue]')
                                    .get('content'))
        try:
            page_data['popularity'] = int(tempsoup.select_one('li.5-star div[class=left]')
                                          .text.replace('(', '').replace(')', ''))
        except ValueError:
            page_data['popularity'] = 0
    except AttributeError:
        page_data['description'] = 'BLOCKED'
        page_data['rating'] = 0.0
        page_data['popularity'] = 0
    return page_data


def get_data(url):
    ignore_plural = {'s', 'y'}
    soup = get_soup(url)
    links = soup.select('a[token=shows-portraits]')
    results = pool.imap(scrape_page, links)
    for result in results:
        for key in ('title', 'description', 'rating', 'popularity', 'numvideos'):
            data_key = key + 's' if key[-1] not in ignore_plural else key
            data[data_key].append(result[key])


def export_csv(output, file):
    with open('output/' + file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(('Title', 'Rating', 'Popularity', 'Videos', 'Description'))
        csv_writer.writerows(output)


def export_sql_and_html(csv_file, season, ajax_season):
    html_file = 'crunchyroll_%s.html' % season
    table_name = 'c_%s' % ajax_season
    os.chdir('output')
    with open('sqlite_script.sql', 'w') as f:
        f.write('\n'.join((
            '.mode csv',
            'BEGIN TRANSACTION;',
            'DROP TABLE IF EXISTS %s;' % table_name,
            '.import %s temp_table' % (csv_file),
            'CREATE TABLE %s (Title TEXT, Rating REAL, Popularity INTEGER, Videos INTEGER, Description TEXT);' % table_name,
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


def main(season, ajax_season, test_sql=False):
    url = 'http://www.crunchyroll.com/videos/anime/seasons/' + season
    extra = 'http://www.crunchyroll.com/videos/anime/seasons/ajax_page?pg=1&tagged%5B%5D=season%3A' + ajax_season
    csv_file = 'crunchyroll_%s.csv' % (season)
    if not test_sql:
        get_data(url)
        get_data(extra)
        print('Saving...')
        zipped = zip(data['titles'], data['ratings'], data['popularity'],
                     data['numvideos'], data['descriptions'])
        zipped = sorted(zipped, key=lambda row: (row[1], row[2]), reverse=True)
        export_csv(zipped, csv_file)
    export_sql_and_html(csv_file, season, ajax_season)


if __name__ == '__main__':
    usage = 'Usage: python crunchyroll.py [season]-[year]'
    try:
        season = sys.argv[1]
        test_sql = True if len(sys.argv) > 2 and sys.argv[2] == '-t' else False
    except IndexError:
        sys.exit(usage)
    if '-' not in season:
        sys.exit(usage)
    ajax_season = '_'.join(season.split('-'))
    main(season, ajax_season, test_sql)
