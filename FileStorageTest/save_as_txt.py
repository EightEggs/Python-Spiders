import re
from turtle import pu
import requests
from pyquery import PyQuery

url = 'https://ssr1.scrape.center'
html = requests.get(url).text
doc = PyQuery(html)
items = doc('.el-card').items()

with open('movies.txt', 'w', encoding='utf-8') as file:
    file.write('+'+'-'*42+'\n')
    for i in items:
        name = i.find('a > h2').text()
        cate = [i.text() for i in i.find('.categories button span').items()]
        published_at = i.find('.info:contains(上映)').text()
        published_at = re.search(r'(\d{4}-\d{2}-\d{2})', published_at).group(1)\
            if published_at and re.search(r'(\d{4}-\d{2}-\d{2})', published_at) else 'Unknown'
        score = i.find('p.score').text()
        file.write(f'|名称: {name}\n')
        file.write(f'|类别: {cate}\n')
        file.write(f'|上映时间: {published_at}\n')
        file.write(f'|评分: {score}\n')
        file.write('+'+'-'*42+'\n')
