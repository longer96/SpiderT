import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
from TBselenium.Config import *
import pymongo
from selenium.webdriver.chrome.options import Options

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


def search():
    driver.get('https://www.jd.com/')
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button")))
        input.send_keys(KEY_WORD)
        submit.click()

        item = driver.find_elements_by_class_name('gl-item')
        var = 1
        while var == 3 or len(item) == 30:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)
            item = driver.find_elements_by_class_name('gl-item')
            # print(len(item))
            var = var + 1

        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b")))

        get_product()
        return total.text

    except TimeoutError:
        search()
        print("出错")


def next_page(page_mub):
    try:
        item = driver.find_elements_by_class_name('gl-item')
        print(len(item))
        var = 1
        while var == 3 or len(item) == 30:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)
            item = driver.find_elements_by_class_name('gl-item')
            print(len(item))
            var = var + 1

        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a")))

        input.clear()
        input.send_keys(page_mub)
        driver.execute_script("arguments[0].scrollIntoView()", submit);
        submit.click()
        time.sleep(0.5)
        text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr')))
        print('当前第几页：' + text.text)

        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.curr"), str(page_mub)))
        get_product()
    except TimeoutError:
        next_page(page_mub)


def get_product():
    print('进来了')
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_goodsList > ul")))
    html = driver.page_source
    doc = pq(html)
    items = doc('#J_goodsList .clearfix .gl-item .gl-i-wrap').items()
    for item in items:
        pro = str(item.html())
        pro = re.sub(' data-lazy-img', 'src', pro)
        # print(pro)
        pattern = re.compile('img.*?src="/(.*?)".*?p-price.*?i>(.*?)</i>.*?p-name.*?title="(.*?)" href', re.S)
        result = re.search(pattern, pro)
        product = {
            'image': result.group(1),
            'price': result.group(2),
            'title': result.group(3)
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(reslut):
    try:
        if db[MONGO_TABLE].insert_one(reslut):
            print('保存成功！')
    except Exception:
        print('保存失败！')


def main():
    try:
        totle = int(search())
        print(totle)
        for i in range(2, totle + 1):
            next_page(i)
    except Exception:
        print('出错啦！')
    finally:
        driver.close()


if __name__ == '__main__':
    main()
