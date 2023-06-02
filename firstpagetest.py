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

# def click_sale_tab ():
#     tab_element = driver.find_element(By.CSS_SELECTOR, '.myptab.typ3')
#     # 1+1, 2+1, 덤증정 행사 => 3번 반복
#     # 전체는 중복되므로 필요없다고 판단
#     tab_list = tab_element.find_elements(By.CSS_SELECTOR, 'li')
#
#     for i in range(len(tab_list)-1):
#         tab_list[i].click()
#         #탭 3개 클릭 확인
#         time.sleep(2)
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
    # paging_element = driver.find_element(By.CSS_SELECTOR, '.num')
    paging_element = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[3]/div/div/div[1]/div/span')

    # //*[@id="contents"]/div[2]/div[3]/div/div/div[1]/div/span
    # //*[@id="contents"]/div[2]/div[3]/div/div/div[2]/div/span

    # 페이지 번호를 클릭
    page_links = paging_element.find_elements(By.CSS_SELECTOR, 'a')
    # print("page_number : "+str(page_number))
    page_links[page_number].click()
    print("대기중")
    # 클릭 후 렌더링 위해 대기
    time.sleep(2)

# 소스코드 가져와서 P태그 선택
def readSourceAndParseTargetTag():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    product_li = soup.select(
        '#contents > div.cnt > div.cnt_section.mt50 > div > div > div:nth-child(3) > ul > li')
    # print(product_li)
    return product_li

def makeItem():
    product_list = readSourceAndParseTargetTag()

    for li in product_list:
        print(find_info(li))
        data.append(find_info(li))

data = []

driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods')
# for i in range(1,3):
#     click_page_number(i)

# click_sale_tab()
print('first=' * 30)
makeItem()

for i in range(1, 10):
    print(str(i) + ' loop=' * 30)
    click_page_number(i)
    makeItem()

driver.quit()

# with open('GS25ver2.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent='\t')
