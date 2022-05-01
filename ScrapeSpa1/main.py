import json
import requests
import logging
from os import makedirs
from os.path import exists

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
LIMIT = 10
TOTAL_PAGE = 10

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def scrape_api(url):
    logging.info('Scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('Get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException as e:
        logging.error(e)


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=(page-1)*LIMIT)
    return scrape_api(url)


def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


def main():
    for page in range(1, TOTAL_PAGE+1):
        index_data = scrape_index(page)
        for item in index_data['results']:
            id = item['id']
            detail_data = scrape_detail(id)
            # logging.info(detail_data)
            save_data(detail_data)


if __name__ == '__main__':
    main()
