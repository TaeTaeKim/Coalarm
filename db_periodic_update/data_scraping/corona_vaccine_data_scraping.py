
import time
import re
import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

# 1-1 vaccine data scraping
def get_vaccine_scraping():

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    # driver 실행
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get('https://ourworldindata.org/covid-vaccinations')
    time.sleep(1)

    #창크기 늘림 EC2 대비
    #driver.set_window_position(0, 0)
    #driver.set_window_size(3000, 3000)

    scroll_table = driver.find_element_by_xpath('//*[@id="the-our-world-in-data-covid-vaccination-data"]')
    action = ActionChains(driver)
    action.move_to_element(scroll_table).perform()
    time.sleep(1)

    click_table = driver.find_element_by_xpath('/html/body/main/article/div[3]/div[2]/div/div/section[1]/figure/div/div[3]/div/div[3]/div[2]/nav/ul/li[2]/a')
    click_table.click()
    time.sleep(1)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    vaccine_datas = []
    Table = soup.find("table",{"class":"data-table"})
    trs = trs = Table.tbody.select('tr')

    for tr in trs:
        vaccine_country = tr.select('td')[0].text
        fully = re.sub(r'[a-zA-z]+ \d{1,2}|, \d{4} |\b%', '',tr.select('td')[1].text)
        if fully == "":
            fully = -1
        elif fully == "<0.01":
            fully = 0
        partly = re.sub(r'[a-zA-z]+ \d{1,2}|, \d{4} |\b%', '',tr.select('td')[2].text)
        if partly == "":
            partly = -1
        elif partly == "<0.01":
            partly = 0
        vaccine_dict = {"country" : vaccine_country, "partly" : partly, "fully" : fully}
        vaccine_datas.append(vaccine_dict)
    return vaccine_datas
