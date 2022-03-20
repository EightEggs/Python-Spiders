import json
import logging
import multiprocessing
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
import requests
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def scrape_page(url):
    """
    scrape page by url and return its html
    :param url: page url
    :return: html of page
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """
    scrape index page and return its html
    :param page: page of index page
    :return: html of index page
    """
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


def parse_index(html):
    """
    parse index page and return detail url
    :param html: html of index page
    """
    pattern = re.compile(r'<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    """
    scrape detail page and return its html
    :param page: page of detail page
    :return: html of detail page
    """
    return scrape_page(url)


def parse_detail(html):
    """
    parse detail page
    :param html: html of detail page
    :return: data
    """

    cover_pattern = re.compile(
        r'class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    name_pattern = re.compile(r'<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile(
        r'<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s?上映')
    drama_pattern = re.compile(r'<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile(r'<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(
        1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(
        1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(
        categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(
        1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(
        1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()
                  ) if re.search(score_pattern, html) else None

    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def save_data(data):
    """
    save to json file
    :param data:
    :return:
    """
    # there is no ':' allowed in file name on Windows
    name = re.sub(r'[:：\s]', '_', data['name'])
    data_path = f'{RESULTS_DIR}/{name}.json'
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main(page):
    """
    main process
    :return:
    """
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
