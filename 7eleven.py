from selenium import webdriver
import json

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get('https://www.7-eleven.co.kr/product/presentList.asp')  # 세븐일레븐 행사상품 링크

data = []


def click_more_items():
    moreitem = driver.find_element(By.CSS_SELECTOR, '#listUl > li.btn_more > a')
    moreitem.click()
    time.sleep(3)

def find_info(li):
    item = {}

    item_img = li.find('img')['src']
    item_title = li.find('div', class_='name').text
    item_price = li.find('div', class_='price').text.strip() + "원"
    if count==0:
        item_sale = li.find('li', class_='ico_tag_06').text.strip()
    else:
        item_sale = li.find('li', class_='ico_tag_07').text.strip()

    item['img'] = 'https://www.7-eleven.co.kr'+item_img   #앞에 세븐일레븐 링크 붙여야 이미지가 나옴
    item['title'] = item_title
    item['price'] = item_price
    item['sale'] = item_sale


    return item  # { } 형태로 반환

def readSourceAndParseTargetTag():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    product_list = soup.select('#listUl > li')  #각 상품의 li 태그가 list로 반환

    # print("="*30+"product_list의 타입"+"="*30)
    # print(type(product_list)) #<class 'bs4.element.ResultSet'>
    return product_list
def makeItem():
    # tab에 list가 담겨짐
    product_list = readSourceAndParseTargetTag()
    del product_list[0]
    product_list.pop()
    # print(product_list)

    for li in product_list:
        print(find_info(li))
        data.append(find_info(li))


for i in range(2): #  0, 1
    count = i
    print("="*30+str(i+1)+"번째 시도"+"="*30)
    # 만약 2회차 반복때는 2+1 탭을 클릭
    if i==1:
        eventtab = driver.find_element(By.CSS_SELECTOR, '#actFrm > div.cont_body > div.wrap_tab > ul > li:nth-child(2) > a')
        eventtab.click()
        time.sleep(3)

    # 페이지 처음 로딩은 1+1행사 탭에서
    # 각 행사에서 더보기를 3번 진행하고 크롤링을 진행
    for k in range(3):
        click_more_items()

    #아이템 크롤링
    makeItem()


    # print(readSourceAndParseTargetTag())

driver.quit()

with open('json_csv/7eleven.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent='\t')

# with open('json_csv/7eleven.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # 데이터 개수 출력
# num_data = len(data)
# print("Number of data: ", num_data)