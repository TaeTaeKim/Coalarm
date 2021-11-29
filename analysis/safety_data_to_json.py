#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:39:49 2021

@author: bizzy
"""

from selenium import webdriver
# from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import time
import json
    
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

# driver 실행
# driver = webdriver.Chrome('./chromedriver.exe', options=options)
# 맥에서 실행 안될 때 터미널에서 chromedriver 위치한 폴더 들어가 입력
# xattr -d com.apple.quarantine chromedriver_m1
# driver = webdriver.Chrome('./chromedriver_m1', options=options)
# 맥에서 실행 안될 때 터미널에서 chromedriver 위치한 폴더 들어가 입력
# xattr -d com.apple.quarantine chromedriver_intel
driver = webdriver.Chrome('./chromedriver/chromedriver_intel', options=options)
driver.implicitly_wait(3)

driver.get('https://globalresidenceindex.com/hnwi-index/safety-index/')
time.sleep(2)

select = Select(driver.find_element_by_name('supsystic-table-14_length'))
select.select_by_visible_text('All')
select.select_by_value('-1')

html = driver.page_source


soup = BeautifulSoup(html, "html.parser")
table = soup.select_one('#supsystic-table-14')
trs = table.tbody.select('tr')

result = []
for tr in trs:
    a = {}
    a['country'] = tr.select('td')[1].text
    a['homicide_rate'] = tr.select('td')[5].text
    result.append(a)

# ISO 코드 추가
with open('./json/country_ISO.json', 'r') as f:
    iso = json.load(f)

for r in result:
    for i in iso:
        if r['country'] == i['Name']:
            r['iso_code'] = i['Code']


with open('./json/safety_data.json', 'w') as f:
    json.dump(result, f)
