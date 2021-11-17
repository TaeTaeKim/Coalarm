from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver import ActionChains
import re

driver = webdriver.Chrome(r'C:\Users\uss\AppData\Local\Programs\Python\Python37\chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://tradingeconomics.com/country-list/terrorism-index')
time.sleep(1)

html = driver.page_source

import requests
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
terrorism_dict = {}
terrorism_datas = []
terrorism_columns = ['Ranking', 'Country', 'Last', 'Previous']
Table = soup.select_one('#ctl00_ContentPlaceHolder1_ctl01_UpdatePanel1 > div > div > table')
trs = Table.tbody.select('tr')
pattern = re.compile(r"([a-zA-Z]+\s?|\d\.?)*")

for r, tr in enumerate(trs):
    Ranking = r + 1
    Country = (tr.select('td')[0].text).strip()
    Last = tr.select('td')[1].text
    Previous = tr.select('td')[2].text

    terrorism_dict_value = [str(Ranking), Country, Last, Previous]
    for i in range(len(terrorism_dict_value)):
        terrorism_dict[terrorism_columns[i]] = pattern.search(terrorism_dict_value[i]).group()
    terrorism_datas.append(dict(terrorism_dict))
print(len(terrorism_datas))

# 163개
terrorism_json_data = json.dumps(terrorism_datas)
print(terrorism_json_data)
