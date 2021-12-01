from selenium import webdriver
import time
import re

def get_terror_data(): # return : ['Ranking', 'Country', 'Last', 'Previous']
   
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    # driver 실행
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome(options=options)

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
    # print(len(terrorism_datas))

    # # 163개
    # terrorism_json_data = json.dumps(terrorism_datas)
    # print(terrorism_json_data)
    return terrorism_datas
