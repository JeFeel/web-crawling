from selenium import webdriver
import json

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()


# 선택자에서 데이터 파싱
def find_info(li):
    item = {}
    p_list = li.select('p')

    img_url = p_list[0].find('img')['src']
    title = p_list[1].text
    price = p_list[2].text
    sale = p_list[3].text

    item['img'] = img_url
    item['title'] = title
    item['price'] = price
    item['sale'] = sale
    return item  # { } 형태로 반환


# 페이지를 클릭하고 렌더링
def click_page_number(page_number):

    paging_element = driver.find_element(By.CSS_SELECTOR, '.num')

    # 페이지 번호를 클릭
    page_links = paging_element.find_elements(By.CSS_SELECTOR, 'a')
    # print("page_number : "+str(page_number))
    page_links[page_number].click()

    # 클릭 후 렌더링 위해 대기
    time.sleep(2)


# 소스코드 가져와서 P태그 선택
def readSourceAndParseTargetTag(index):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    if index == 0:
        product_li = soup.select(
            '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(3) > ul > li')
    elif index == 1:
        product_li = soup.select(
            '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(5) > ul > li')
    else:
        print("에러 발생")

    # 3 5 7로 변해서 각각의 탭에서 데이터를 파싱해야됨
    return product_li


def makeItem(tag):
    #product_li를 전달받음
    # product_list = readSourceAndParseTargetTag()
    product_list = tag

    for li in product_list:
        print(find_info(li))
        data.append(find_info(li))

data = []

driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods')

# 탭을 클릭한 후, 해당 탭에서 10페이지 분량의 데이터를 크롤링
tab_element = driver.find_element(By.CSS_SELECTOR, '.myptab.typ3')
# 1+1, 2+1 행사 => 2번 반복
# 전체는 중복되므로 필요없다고 판단
tab_list = tab_element.find_elements(By.CSS_SELECTOR, 'li')

for i in range(2):
    # 0 1
    tab_list[i].click()
    # 탭 3개 클릭 확인
    time.sleep(2)
    tag = readSourceAndParseTargetTag(i) #return된 product_li가 변수에 저장됨

    print('first=' * 30)
    # 첫 페이지의 makeItem
    makeItem(tag)

    for k in range(1, 10):
        print(str(k) + ' loop=' * 30)
        click_page_number(k)
        makeItem(tag)

    # page_list = soup.select(
    #     '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(3) > div > span > a')

driver.quit()

with open('GS25.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent='\t')
