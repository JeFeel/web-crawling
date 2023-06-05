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

# def click_sale_tab (n):
#     # tab_element = driver.find_element(By.CSS_SELECTOR, '.myptab.typ3')
#     #contents > div.cnt > div.cnt_section.mt50 > div > div > ul > li
#     tab_list = htmlsoup().select('#contents > div.cnt > div.cnt_section.mt50 > div > div > ul > li')
#     print(tab_list[n])
#     # tab_list[n].find_element('a').click()
#     #클릭 후 렌더링 시간
#     time.sleep(2)

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
    item['csv'] = "GS25"
    return item  # { } 형태로 반환


# 페이지를 클릭하고 렌더링
def click_page_number(n, page_number):
    # paging_element = driver.find_element(By.CSS_SELECTOR, '.num')
    if (n == 0):
        paging_element = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[3]/div/div/div[1]/div/span')
    else:
        paging_element = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[3]/div/div/div[2]/div/span')

    # 페이지 번호를 클릭
    page_links = paging_element.find_elements(By.CSS_SELECTOR, 'a')
    # print("page_number : "+str(page_number))
    page_links[page_number].click()
    print("대기중")
    # 클릭 후 렌더링 위해 대기
    time.sleep(2)


# def htmlsoup():
#     html = driver.page_source
#     soup = BeautifulSoup(html, "html.parser")
#     return soup

# 소스코드 가져와서 P태그 선택
def readSourceAndParseTargetTag(n):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # product_li = soup.select(
    #     '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(3) > ul > li')

    if n == 0:
        # 1+1 행사인 경우의 li 리스트
        product_li = soup.select('#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(3) > ul > li')
    else:
        # 2+1 행사인 경우의 li 리스트
        product_li = soup.select('#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(5) > ul > li')

    # print(product_li)
    return product_li


def makeItem(n):
    # tab에 list가 담겨짐
    product_list = readSourceAndParseTargetTag(n)

    for li in product_list:
        print(find_info(li))
        data.append(find_info(li))


data = []
driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods')

# 1+1탭인지 2+1탭인지
# 0,1
for n in range(2):
    if n == 1 :
        selectevent = driver.find_element(By.CSS_SELECTOR, '#contents > div.cnt > div.cnt_section.mt50 > div > div > ul > li:nth-child(2) > span')
        selectevent.click()
        time.sleep(3)

    # selectevent[n] #<li><span class="active"><a href="#;" id="ONE_TO_ONE">1+1 행사</a></span></li>
    # 탭을 클릭한 후 페이지 로드해서 파싱 시작

    print('first=' * 30)
    makeItem(n)

    for i in range(1, 10):
        print(str(i) + ' loop=' * 30)
        click_page_number(n, i)
        makeItem(n)


driver.quit()

with open('json_csv/GS25.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent='\t')
