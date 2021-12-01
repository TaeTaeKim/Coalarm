from selenium import webdriver
from selenium.webdriver.support.select import Select
import re
import time

def get_safety_data(): # return : ['Country', 'Safety_index', 'Numbeo_index', 'Homicide_rate']
    
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    
    # driver 실행
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome(options=options)
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

    pd.set_option('display.max_row', 500)

    df = pd.read_json(Safety_json_data)

    duplicate_sum = (df.groupby(['Country'], as_index=False).mean()).round(2)

    duplicate_sum_json = duplicate_sum.to_dict('records')

    return duplicate_sum_json
