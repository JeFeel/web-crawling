from selenium import webdriver
import json

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get('https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N')  #CU 행사상품 링크

data = []

# print(soup.select('#contents > div.depth3Lnb > ul > li'))  #eventinfo 태그 3개가 list로 반환됨
def readSourceAndParseTargetTag():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    product_list = soup.select('#contents > div.relCon > div > ul > li > a')  #각 상품의 a 태그가 list로 반환
    # print("="*30+"product_list의 타입"+"="*30)
    # print(type(product_list)) #<class 'bs4.element.ResultSet'>
    return product_list

def find_info(li):
    item = {}

    item_img = li.find('img')['src']
    item_title = li.find('div', class_='name').text
    item_price = li.find('div', class_='price').text
    item_sale = li.find('div', class_='badge').text.strip()
    item['img'] = item_img
    item['title'] = item_title
    item['price'] = item_price
    item['sale'] = item_sale
    item['csv'] = "CU"



    return item  # { } 형태로 반환

def makeItem():
        # tab에 list가 담겨짐
    product_list = readSourceAndParseTargetTag()

    for li in product_list:
        print(find_info(li))
        data.append(find_info(li))


for i in range(2): #  0, 1
# 1+1, 2+1 탭을 클릭후 비동기 처리로 로딩되는 페이지의 정보를 읽어들인다
    if(i==0):
        eventlist =driver.find_element(By.CSS_SELECTOR, '#contents > div.depth3Lnb > ul > li.eventInfo_02 > a')
    else:
        eventlist =driver.find_element(By.CSS_SELECTOR, '#contents > div.depth3Lnb > ul > li.eventInfo_03 > a')

    eventlist.click()
    time.sleep(3)  #클릭 후 페이지 로딩 기다림

    print("="*30+str(i+1)+"번째 시도"+"="*30)
    # print(readSourceAndParseTargetTag())

    # 이하 파싱 시작
    makeItem()



driver.quit()

with open('json_csv/CUcsv.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent='\t')

# with open('CUcsv.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # 데이터 개수 출력
# num_data = len(data)
# print("Number of data: ", num_data)