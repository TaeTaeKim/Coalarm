import requests
import json
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
# Select tag의 값을 선택
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def get_embassy_data(): # return column : ['country_eng_nm', 'country_iso_alp2', 'country_nm', 'embassy_kor_nm', 'url']
    url = 'http://apis.data.go.kr/1262000/EmbassyService2/getEmbassyList2'
    key = '8F5UsoNlidAdZH5ST1vWuuwi6Q9KPRckgXs6utce+UxEZg4g8Mc7ltUGjAj0HU0TKE7993tWHmiD7bskyWMa6Q=='
    
    params ={
        'serviceKey' : key, 
        'pageNo' : '1', 
        'numOfRows' : '300'
    }

    response = requests.get(url, params=params)
    data = str(response.text)
    data = json.loads(data)['data']

    for d in data:
        d.pop('center_tel_no')
        d.pop('embassy_lat')
        d.pop('embassy_lng')
        d.pop('embassy_manage_ty_cd')
        d.pop('embassy_manage_ty_cd_nm')
        d.pop('embassy_cd')
        d.pop('emblgbd_addr')
        d.pop('tel_no')
        d.pop('urgency_tel_no')
        d.pop('embassy_ty_cd')
        d.pop('embassy_ty_cd_nm')
        d.pop('free_tel_no')

    data2 = []
    for d in data:
        if d not in data2:
            data2.append(d)


    URL = 'https://www.mofa.go.kr/www/pgm/m_4179/uss/emblgbd/emblgbdAdres.do'
    
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    # driver 실행
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome(options=options)
    driver.get(url=URL)
    # Select tag 에서 '100 개씩 조회' 선택 
    select = Select(driver.find_element_by_xpath('//*[@id="sub_content"]/form/div/div/select'))
    select.select_by_value('100')
    time.sleep(1)
    # '100 개씩 조회' 적용 
    click_table = driver.find_element_by_xpath('//*[@id="sub_content"]/form/div/div/button')
    click_table.click()
    time.sleep(1)
    # 1 페이지 HTML 저장
    html_1 = driver.page_source
    # 1 페이지 스크롤
    some_tag = driver.find_element_by_xpath('//*[@id="sub_content"]/div[2]/a[2]')
    action = ActionChains(driver)
    action.move_to_element(some_tag).perform()
    time.sleep(1)
    # 2 페이지 넘어가기
    click_table = driver.find_element_by_xpath('//*[@id="sub_content"]/div[2]/a[2]')
    click_table.click()
    time.sleep(1)
    # 2 페이지 HTML 저장
    html_2 = driver.page_source


    soup = BeautifulSoup(html_1, "html.parser")
    table_list = soup.find("div",{"class":"table_list"})
    tables = table_list.select('table')

    # {'이름': URL}
    url = {}
    for t in tables:
        url[t.find('a').text] = t.find('a')['href']


    soup = BeautifulSoup(html_2, "html.parser")
    table_list = soup.find("div",{"class":"table_list"})
    tables = table_list.select('table')

    for t in tables:
        url[t.find('a').text] = t.find('a')['href']

    # URL 추가
    new = []
    for d in data2:
        if d['embassy_kor_nm'] in url:
            d['url'] = url[d['embassy_kor_nm']]
            new.append(d)

    return new
