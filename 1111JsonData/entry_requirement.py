#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:39:33 2021

@author: bizzy
"""
# https://www.data.go.kr/data/15085787/openapi.do

import requests
import threading
import json
from bs4 import BeautifulSoup

class AsyncTask:

    def __init__(self):
        pass

    def Entry(self):    # 나라 - text, 주기 : 15
        threading.Timer(15,self.Entry).start()

        url = 'http://apis.data.go.kr/1262000/CountryOverseasArrivalsService/getCountryOverseasArrivalsList'
        params ={
            'serviceKey' : "Sk4Syk+ddhdzDzSKdby8eRCdDfe912d+TxPmhp7Uq2UoxKrXMqgSQDv1vLQsOknyyNqHVICzTmwubry2uL7vig==",
            'pageNo': 1,
            'numOfRows': 200
        }
        
        response = requests.get(url, params=params)
        response_text = response.text
        response_text_dict = eval(response_text)
        data_text = response_text_dict['data']
        
        for er in data_text:
            er['country_name'] = er.pop('country_eng_nm')
            er['entry_requirement'] = er.pop('txt_origin_cn')
            er.pop('country_nm')
            er.pop('html_origin_cn')
            er.pop('notice_id')
            er.pop('title')
        
        url = 'http://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2'
        params ={'serviceKey' : 'l2Tz12aLRivDhn4CKg0XE5RGdY4wc7asf9UaKQmF6ZRiigW0klMF5ioFkBI47WiY0XTahwpsqMYX1l9Kl6gaWg==',
                'returnType' : 'JSON',
                'numOfRows' : '200',
                'pageNo' : '1' }

        response = requests.get(url, params=params)
        result =response.json()
        data= result['data']

        dict_list = []
        for r in data:
            if r['alarm_lvl'] != None:
                key = r['country_iso_alp2']
                value = r['alarm_lvl']
                dict_list.append({'country_iso_alp2' : key, 'alarm_lvl' : value})

        #data_text : 'text', dict_list : 'alarm_lvl'  , join : 'country_iso_alp2'
        for i in data_text:
            i["alarm_lvl"] = "위험"
            for j in dict_list:
                if i['country_iso_alp2'] == j['country_iso_alp2']:
                    i["alarm_lvl"] = j["alarm_lvl"]

        # 저장
        file_path = "./corona.json"
        with open(file_path, 'w') as f:
            json.dump(data_text, f)
        print("api 호출 완료")

    def CD(self):   # 나라별 코로나 정보, 주기 12
        threading.Timer(12,self.CD).start()

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
            country_info = {
                    'country_name' : r[2],
                    'confirmed': r[9].replace(",", ""),
                    'death': r[5][:-1].replace(",", ""),
            }
            
            data.append(country_info)
        data = sorted(data, key = lambda x : x["country_name"])
        
        with open('./country_ISO.json', 'r') as f:
            b = json.load(f)
        
        for i in range(len(data)-3):
            data[i]['country_iso_alp2'] = "없음"
            for j in b:
                if data[i]['country_name'] == j['Name']:
                    data[i]['country_iso_alp2'] = j['Code']
            if data[i]['country_iso_alp2'] == "없음":
                data.pop(i)

        # 저장
        file_path = "./sample_data.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print("데이터 스크래핑 완료")