import json
import re
import requests

def get_data():
    fp = open("item.json", 'rb')
    try:
        html = fp.read()
    finally:
        fp.close()
    data = json.loads(html)
    for item in data:
        title = data.get(item).get('title')
        url = data.get(item).get('uri')
        title = re.sub(' \d.*', "", title).strip()
        title = re.sub('\?', "", title).strip()
        info = {
            'url': url,
            'title': title
        }
        write_to_file(info)
        save_img(info)


def write_to_file(info):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(info, ensure_ascii=False) + '\n')
        f.close()


def save_img(info):
    name = info['title']
    url = info['url']
    headers = {
        'Host': 'static.wixstatic.com',
        'User-Agent': 'Mozilla/4.0 (Windows NT 8.0; Win64; x64; rv:57.0) Gecko/20120101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    print('正在保存：', name, 'https://static.wixstatic.com/media/' + info.get('url'))
    try:
        content = requests.get('https://static.wixstatic.com/media/' + info.get('url'), headers=headers).content
        with open(name + url, 'wb') as f:
            f.write(content)
            f.close()
    except:
        print('连接错误！')
        save_img(info)



if __name__ == '__main__':
    get_data()
