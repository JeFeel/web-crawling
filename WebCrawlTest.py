from urllib.request import urlopen

import requests
import json
from bs4 import BeautifulSoup
import requests as req

url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods'
res = requests.get(url)
# print(res.text)

bsObject = BeautifulSoup(res.text, "html.parser")

product_ul = bsObject.select('.mdprod_list > li')

data = []

for idx in range(len(product_ul)):
    item = {}
    item['title'] = product_ul[idx].select_one('p.tit').text
    item['img'] = product_ul[idx].select_one('p.img > img').get('src')
    item['sale'] = product_ul[idx].select_one('p.flg02 > span ').text
    item['price'] = product_ul[idx].select_one('p.price > span.cost').text.strip()
    data.append(item)

# JSON 파일로 저장
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent='\t')

# print(product_ul)
# print(len(product_ul))

# for idx in range(len(product_ul)):
#     title = product_ul[idx].select_one('p.tit')
#     img = product_ul[idx].select_one('p.img > img').get('src')
#     sale = product_ul[idx].select_one('p.flg02 > span ').text
#
#     item = {'상품명': title, '상품사진': img, '할인': sale}
#     with open("data.json", "w", encoding = 'utf-8') as f:
#         json.dump(item, f)
#
#
#     print(title.text)
#     print(img)
#     print(sale)

# driver.get('https://sports.news.naver.com/wfootball/index')

# for i in range(1, 10):
#     article = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div[2]/div/ol/li[{i}]/a')
#     article.click()
#     time.sleep(1)
#
#     # 데이터파싱
#     parseHtml = driver.page_source
#     print(parseHtml)
#
#     driver.back()
#     time.sleep(2)
#
# # 페이지가 완전히 로딩되도록 3초동안 기다림
# time.sleep(3)
