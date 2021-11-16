#딕셔너리화, 스크롤링,regex(compile, search), JSON dumps 연습
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import re

driver = webdriver.Chrome(r'C:\Users\uss\AppData\Local\Programs\Python\Python37\chromedriver.exe')
driver.implicitly_wait(3)

driver.get('https://coronaboard.kr/en/')
time.sleep(1)

for i in range(2):
    #some_element까지 스크롤
    some_element = driver.find_element_by_xpath('//*[@id="global-slide"]/div/div[3]/p/a')
    action = ActionChains(driver)
    action.move_to_element(some_element).perform()
    time.sleep(0.1)

    #더보기 클릭
    more_data = driver.find_element_by_xpath('//*[@id="show-more"]')
    more_data.click()
    time.sleep(0.1)

#페이지 소스 html변수에 저장
html = driver.page_source

import requests
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
board_dict = {}
board_datas = []
board_columns = ['country', 'Confirmed', 'Deaths', 'Recovered', 'Fatality', 'Recovery', 'Incidence']
Table = soup.find("table",{"class":"google-visualization-table-table"})
trs = trs = Table.tbody.select('tr')
#regex
pattern = re.compile(r"(\(?\+?\d\)?\.?\,?|\s?[a-z\/A-Z]\.?|-?|[a-zA-Z])*")
for tr in trs:
    country = tr.select('td')[1].text
    Confirmed = tr.select('td')[2].text
    Deaths = tr.select('td')[3].text
    Recovered = tr.select('td')[4].text
    Fatality = tr.select('td')[5].text
    Recovery = tr.select('td')[6].text
    Incidence = tr.select('td')[7].text
    board_dict_value = [country, Confirmed, Deaths, Recovered, Fatality, Recovery, Incidence]
    for i in range(len(board_dict_value)):
        board_dict[board_columns[i]] = pattern.search(board_dict_value[i]).group()
        if board_dict[board_columns[i]] == '-' or board_dict[board_columns[i]] == 'N/A':
            board_dict[board_columns[i]] = -1
    board_datas.append(dict(board_dict))
#국가 수
print(len(board_datas))
#JSON
vaccine_json_data = json.dumps(board_datas)
print(vaccine_json_data)
