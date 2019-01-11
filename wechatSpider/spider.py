from urllib.parse import urlencode

import requests
from requests.exceptions import ConnectionError

key_word = '单反'
base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'IPLOC=CN5101; SUID=C11672763120910A000000005BFFA463; SUV=1543480421705510; SNUID=4F9BFCFB8D8BF6441E9AF2208E90A4DC; ABTEST=0|1543480521|v1; JSESSIONID=aaaR_em5ZWGyAcHrAy6Cw; com_sohu_websearch_ITEM_PER_PAGE=10; weixinIndexVisited=1; sct=8; ld=jyllllllll2b@fF4lllllVs@IhllllllNXwQZylllltlllll4ylll5@@@@@@@@@@; pgv_pvi=1133113344; pgv_si=s9688569856; LSTMV=235%2C73; LCLKINT=1967; ppinf=5|1543482090|1544691690|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTowOnxjcnQ6MTA6MTU0MzQ4MjA5MHxyZWZuaWNrOjA6fHVzZXJpZDo0NDpvOXQybHVDa3RTSERJazBLWWNKYkQwU3Y5a3pnQHdlaXhpbi5zb2h1LmNvbXw; pprdig=tOIJ_b-_xwHsWZgF8BLWT7_PHVO_SVgWpB7r4JYyVMj6Ccj1xI6Tq8vMufLazXBnDbZasQMumnWJpSHow3rT3sxafM6ruT3PN9DNxUtuvIe4VOQLOZkO4lP4VHIbxRxG588j103Hv9ABQXoOmbtV7acLVXaOROY5j0kTjA1YZX4; sgid=02-36057217-AVvicqupYUlTRk3yVE0J4W4Q; ppmdig=1543481116000000ce18f35efaa17f3ed1c26db432755f3f',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}
proxy_pool_url = 'http://localhost:5000/get'
proxy = None
maxCount = 5


# 得到IP代理
def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('URL:', url)
    print('从新尝试次数', count)
    global proxy
    if count >= maxCount:
        print('请求次数过多！')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 302:
            # 换IP
            print(302)
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url, count)
            else:
                print('Get Proxy Faild')
                return None
    except ConnectionError as e:
        print('Error Occured', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def main():
    for page in range(1, 101):
        html = get_index(key_word, page)
        print(html)


if __name__ == '__main__':
    main()
