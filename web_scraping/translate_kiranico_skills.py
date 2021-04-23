import csv
import sys
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests


def get_soup(url):
    r = requests.get(url)  # Kiranico requires a user agent, which Requests provides by default
    return bs4.BeautifulSoup(r.text, 'html.parser')


def translate_skill(skill_row, language_code):
    link = skill_row.select_one('a')
    en_skill_name = link.get_text()
    href = link['href'].replace('data', language_code + '/data')
    
    try:
        translated_skill_name = get_soup(href).select_one('h1').get_text().strip()
    except AttributeError:
        raise ValueError("unsupported language code")
    
    return en_skill_name, translated_skill_name


def scrape_to_csv(language_code):
    output_path = 'output/kiranico_skills_{}.csv'.format(language_code)
    skills_table = get_soup('https://mhrise.kiranico.com/data/skills').select_one('tbody')
    rows = skills_table.select('tr')
    num_rows = len(rows)
    
    with ThreadPoolExecutor(max_workers=num_rows) as pool:
        results = pool.map(translate_skill, rows, [language_code] * num_rows)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(results)


if __name__ == '__main__':
    try:
        language_code = sys.argv[1]
    except IndexError:
        sys.exit('Usage: python translate_kiranico_skills.py [language code]')
    
    scrape_to_csv(language_code)
