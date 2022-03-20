import requests
import re
import json


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
    name = data['name']
    #!! there is no ':' allowed in file name on Windows !!
    data_path = f'{name}.json'.replace(':', '')
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=4)


if __name__ == '__main__':
    url = 'https://ssr1.scrape.center/detail/16'
    response = requests.get(url)
    data = parse_detail(response.text)
    print(data)
    save_data(data)
