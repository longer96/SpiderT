import json
from urllib.parse import urlencode

import os
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import re
import pymongo
from  jrttjd.config import *
from hashlib import md5


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败！')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 8.1; Win64; x64; rv:57.0) Gecko/2010021101 Firefox/57.0',
            # 'Cookie':'__tasessionId=wruaj3nki1542878166915',
            'Host':'www.toutiao.com'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        return None
    except RequestException:
        return None


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储成功！',result)
        return True
    return False

def parse_page_detail(html,url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile('JSON.parse(.*?)siblingList', re.S)
    result = re.search(image_pattern, html)
    if result:
        # print(result.group(1))
        return {
            'title': title,
            'url' : url,
            'images' : result.group(1)
        }

def save_image(url):
    file_path = '{0}/{1}.{2}'.format(os.getcws(),md5(url).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb')as f:
            f.write(url)
            f.close()


def main():
    html = get_page_index(0, 'GD')
    for url in parse_page_index(html):
        print(url)
        html = get_page_detail(url)
        # print('====================b==================')
        # print(html)
        # print('====2================e==================')
        if html:
            result = parse_page_detail(html,url)
            save_to_mongo(result)

if __name__ == '__main__':
    main()
