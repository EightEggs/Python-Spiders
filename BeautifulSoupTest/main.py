import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def scrape_page(url):
    logging.info('scraping %s...\n', url)
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        logging.error('get invalid status code %s while scraping %s\n',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s\n', url, exc_info=True)


def save_data(data):
    """
    save to json file
    :param data:
    :return:
    """
    data_path = 'result.html'
    with open(data_path, 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    url = 'https://www.gitee.com'
    html = scrape_page(url)
    soup = BeautifulSoup(html, 'lxml')
    save_data(soup.prettify(formatter='html'))
