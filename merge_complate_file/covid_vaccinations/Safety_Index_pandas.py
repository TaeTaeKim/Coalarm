from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
import re
import time

driver = webdriver.Chrome(r'C:\Users\uss\AppData\Local\Programs\Python\Python37\chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://globalresidenceindex.com/hnwi-index/safety-index/')
time.sleep(2)

select = Select(driver.find_element_by_name('supsystic-table-14_length'))
select.select_by_visible_text('All')
select.select_by_value('-1')

html = driver.page_source

import requests
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
Safety_dict = {}
Safety_datas = []
# 국가, 안전지수, 치안지수, 살인률
Safety_columns = ['Country', 'Safety_index', 'Numbeo_index', 'Homicide_rate']
table = soup.select_one('#supsystic-table-14')
trs = table.tbody.select('tr')

pattern = re.compile(r"([a-zA-Z]+\s?|\-?\d\.?)*")

for r, tr in enumerate(trs):
    Country = tr.select('td')[1].text
    Safety_index = tr.select('td')[3].text
    Numbeo_index = tr.select('td')[4].text
    Homicide_rate = tr.select('td')[5].text
    Safety_dict_value = [Country, Safety_index, Numbeo_index, Homicide_rate]
    for i in range(len(Safety_dict_value)):
        Safety_dict[Safety_columns[i]] = pattern.search(Safety_dict_value[i]).group()
    Safety_datas.append(dict(Safety_dict))
Safety_json_data = json.dumps(Safety_datas)

import pandas as pd
from pandas import json_normalize

print("pandas version: ", pd.__version__)
pd.set_option('display.max_row', 500)

df = pd.read_json(Safety_json_data)
duplicate_sum = (df.groupby(['Country'], as_index=False).mean()).round(2)

duplicate_sum_json = duplicate_sum.to_json(orient = 'records')
print(duplicate_sum_json)

# 181개 ->
# print(df.head(len(df)))
# -> 130개
# print(duplicate_values_sum.head(len(duplicate_values_sum)))
