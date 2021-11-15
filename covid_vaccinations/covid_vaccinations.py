from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import re
import time
import json

driver = webdriver.Chrome(r'C:\Users\uss\AppData\Local\Programs\Python\Python37\chromedriver.exe')
driver.implicitly_wait(3)

driver.get('https://ourworldindata.org/covid-vaccinations')
time.sleep(0.5)

#창크기 늘림 EC2 대비
#driver.set_window_position(0, 0)
#driver.set_window_size(3000, 3000)

scroll_table = driver.find_element_by_xpath('//*[@id="the-our-world-in-data-covid-vaccination-data"]')
action = ActionChains(driver)
action.move_to_element(scroll_table).perform()
time.sleep(0.3)

click_table = driver.find_element_by_xpath('/html/body/main/article/div[3]/div[2]/div/div/section[1]/figure/div/div[3]/div/div[3]/div[2]/nav/ul/li[2]/a')
click_table.click()
time.sleep(0.1)

html = driver.page_source

#크롤링
import requests
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
vaccine_dict = {}
vaccine_datas = []
vaccine_columns = ['country', 'fully', 'partly']
Table = soup.find("table",{"class":"data-table"})
trs = trs = Table.tbody.select('tr')

for tr in trs:
    vaccine_country = tr.select('td')[0].text
    fully = re.sub(r'[a-zA-z]+ \d{1,2}|, \d{4} |\b\%', '',tr.select('td')[1].text)
    partly = re.sub(r'[a-zA-z]+ \d{1,2}|, \d{4} |\b\%', '',tr.select('td')[2].text)
    vaccine_dict_value = [vaccine_country, fully, partly]
    for i in range(3):
        vaccine_dict[vaccine_columns[i]] = vaccine_dict_value[i]
        if vaccine_dict_value[i] == "":
            vaccine_dict[vaccine_columns[i]] = -1
    vaccine_datas.append(dict(vaccine_dict))
#print(vaccine_datas)

vaccine_json_data = json.dumps(vaccine_datas)

print(vaccine_json_data)
