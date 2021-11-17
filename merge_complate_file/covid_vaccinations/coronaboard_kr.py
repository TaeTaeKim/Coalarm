#국내 지역, 확진자, 치료중, 사망자, 격리해제, 치명, 완치, 발생률, 인구수
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver import ActionChains
import re

driver = webdriver.Chrome(r'C:\Users\uss\AppData\Local\Programs\Python\Python37\chromedriver.exe')
driver.implicitly_wait(3)
driver.get('https://coronaboard.kr/en')
time.sleep(3)

some_element = driver.find_element_by_xpath('//*[@id="kr-table"]/div/div/table/thead/tr/th[6]')
action = ActionChains(driver)
action.move_to_element(some_element).perform()
time.sleep(0.1)

select_data = driver.find_element_by_xpath('//*[@id="korea-slide"]/div/div[4]/div/button/div/div/div')
select_data.click()
select_data = driver.find_element_by_xpath('//*[@id="bs-select-2-1"]')
select_data.click()
select_data = driver.find_element_by_xpath('//*[@id="bs-select-2-2"]')
select_data.click()
select_data = driver.find_element_by_xpath('//*[@id="bs-select-2-4"]')
select_data.click()

html = driver.page_source

import requests
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
kr_dict = {}
kr_datas = []
kr_columns = ['Region', 'Confirmed', 'Activecase', 'Deaths', 'Recovered', 'Fatality', 'Recovery', 'Incidence', 'Population']
Table = soup.select_one ('#kr-table > div > div > table')
trs = Table.tbody.select('tr')
pattern = re.compile("(\(?\-?\(?\+?\d\)?\.?\,?|[a-zA-Z]\.?|-?)*")

for tr in trs:
    Region = tr.select('td')[1].text
    Confirmed = tr.select('td')[2].text
    Activecase = tr.select('td')[3].text
    Deaths = tr.select('td')[4].text
    Recovered = tr.select('td')[5].text
    Fatality = tr.select('td')[6].text
    Recovery = tr.select('td')[7].text
    Incidence = tr.select('td')[8].text
    Population = tr.select('td')[9].text
    kr_dict_value = [Region, Confirmed, Activecase, Deaths, Recovered, Fatality, Recovery, Incidence, Population]
    for i in range(len(kr_dict_value)):
        kr_dict[kr_columns[i]] = pattern.search(kr_dict_value[i]).group()
        if kr_dict[kr_columns[i]] == '-' or kr_dict[kr_columns[i]] == 'N/A':
            kr_dict[kr_columns[i]] = 0
    kr_datas.append(dict(kr_dict))
print(len(kr_datas))

vaccine_json_data = json.dumps(kr_datas)
print(vaccine_json_data)