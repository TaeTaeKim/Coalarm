#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 09:58:58 2021

@author: bizzy
"""

import requests
import json
from bs4 import BeautifulSoup

def CD():
    url = "https://www.worldometers.info/coronavirus/"
    html = requests.get(url).text
    
    soup = BeautifulSoup(html, "html.parser")
    # id가 "main_table_countries_today"인 table 가져오기
    tags = soup.find("table", id="main_table_countries_today")
    # table 의 tbody 의 tr 가져오기
    tr = tags.tbody.select('tr')
    
    result = []
    for i in tr:
        result.append(i.text.split('\n'))
    
    data = []
    for r in result[8:]:
        
        # 컬럼 추가 예정
        country_info = {
                'country_name' : r[2],
                'confirmed': r[9].replace(",", ""),
                'death': r[5][:-1].replace(",", ""),
        }
        
        data.append(country_info)
    data = sorted(data, key = lambda x : x["country_name"])
    
    with open('./country_ISO.json', 'r') as f:
        b = json.load(f)
        
    for i in data:
        for j in b:
            if i['country_name'] == j['Name']:
                i['country_iso_alp2'] = j['Code']
    
    return data
            