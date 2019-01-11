import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('class="item".*?em.*?>(.*?)</em>'
                         + '.*?<img.*?src="(.*?)"'
                         + '.*?title">(.*?)</span>'
                         + '.*?bd.*?<p.*?>(.*?)<br>'
                         + '.*?average">(\S+)<'
                         + '.*?<span>(\S+)</span>'
                         + '.*?inq">(.*?)</span>',
                         re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            # 'dy' : item[3].split("导演: ")[1].split("主演:")[0].strip(),
            'actor': item[3].strip(),
            'score': item[4],
            'pj': item[5],
            'qm': item[6]
        }


def write_to_file(content):
    # 防止中文变成Ascii
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://movie.douban.com/top250?start=' + str(offset) + '&filter='
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*20 for i in range(10)])