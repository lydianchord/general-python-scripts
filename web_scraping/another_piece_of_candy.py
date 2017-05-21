import bs4
import io
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from urllib.request import urlopen

HOME = 'http://another-piece-of-candy.thewebcomic.com'
OUTPUT_FOLDER = 'jpg_files'


def get_soup(url):
    with urlopen(url) as resp:
        data = resp.read()
    return bs4.BeautifulSoup(data, 'html.parser')


def save_page_image_as_jpg(page_info):
    num, url = page_info
    jpg_name = '{}.jpg'.format(num)
    
    page_html = get_soup(url)
    image_url = page_html.select_one('#comic_image').get('src')
    
    with urlopen(image_url) as resp:
        data = resp.read()
    with io.BytesIO(data) as stream:
        with Image.open(stream) as img:
            img.save(os.path.join(OUTPUT_FOLDER, jpg_name))
    
    print(jpg_name)


def scrape_all_images():
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    
    home_html = get_soup(HOME)
    jumpbox_options = home_html.select('option.jumpbox_page')
    pages = enumerate((HOME + option.get('value') for option in jumpbox_options), 1)
    
    with ThreadPoolExecutor(max_workers=len(jumpbox_options)) as pool:
        pool.map(save_page_image_as_jpg, pages)


if __name__ == '__main__':
    scrape_all_images()
