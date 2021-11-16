
# https://www.data.go.kr/data/15085787/openapi.do


import requests
import pymysql
import threading
import json
import time
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

# 1 -> 1.1 호출
# 2 -> 2.1 호출
# 3 -> 3.1, 3.2 호출
class AsyncTask:

    def __init__(self):
        print("background thread - db update")

    # 기능 1. scraping vaccine data update, 주기 : 100초
    def update_Corona_Vaccine_Data(self):
        
        # 0. 쓰레드 실행
        threading.Timer(100, self.update_Corona_Vaccine_Data).start()
        
        # 1. scraping
        vaccine_data = self.__get_vaccine_scraping()

        # 2. iso 컬럼 추가
        with open('./json_file/country_ISO.json', 'r') as f:
            iso_list = json.load(f)

        for i in range(len(vaccine_data)):
            vaccine_data[i]["iso_code"] = "없음"
            for j in range(len(iso_list)):
                if vaccine_data[i]["country"] == iso_list[j]["Name"]:
                    vaccine_data[i]["iso_code"] = iso_list[j]["Code"]

        # 3. db 연결
        conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE corona_vaccine_data') # 테이블 레코드 비우기

        # 4. 해당 테이블에 데이터 추가
        for i in range(len(vaccine_data)):
            cur.execute('INSERT INTO corona_vaccine_data VALUES("{0}", "{1}", "{2}", "{3}")'.format(\
            vaccine_data[i]["country"], \
            vaccine_data[i]["iso_code"], \
            float(vaccine_data[i]["partly"]),\
            float(vaccine_data[i]["fully"])))
        conn.commit()
        conn.close()
        print("corona_vaccine_date table update complete")

    # 기능 2. coronaboard scraping, 주기 : 80초
    def update_Corona_Data(self):
        # 0. 쓰레드 실행
        threading.Timer(80, self.update_Corona_Data).start()

        # 1. scraping
        get_corona_data = self.__get_corona_scraping()

        # 2. 중복 나라 제거
        country_list = []
        corona_data = []
        for i in range(len(get_corona_data)):
            if get_corona_data[i]["country_name"] in country_list:
                continue
            country_list.append(get_corona_data[i]["country_name"])
            corona_data.append(get_corona_data[i])

        # 3. iso, continent 컬럼 추가
        with open('./json_file/country_ISO.json', 'r') as f:
            iso_data = json.load(f)

        for i in range(len(corona_data)):
            corona_data[i]['country_iso_alp2'] = "없음"
            for j in iso_data:
                if corona_data[i]['country_name'] == j['Name']:
                    corona_data[i]['country_iso_alp2'] = j['Code']

        with open('./json_file/continent.json', 'r') as f:
            continent = json.load(f)

        # corona_data[i]["continent"]
        for i in range(len(corona_data)):
            corona_data[i]["continent"] = "없음"
            for j in continent:
                if corona_data[i]["country_iso_alp2"] == j["iso_code"]:
                    corona_data[i]["continent"] = j["continent"]

        # 4. db 연결
        conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE corona_data') # 테이블 레코드 비우기
        
        # 5. 해당 테이블에 데이터 추가
        for i in range(len(corona_data)):
            cur.execute('INSERT INTO corona_data VALUES("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}", "{11}")'.format(\
            corona_data[i]["country_name"], \
            corona_data[i]["country_iso_alp2"], \
            corona_data[i]["continent"], \
            int(corona_data[i]["total_confirmed"]), \
            int(corona_data[i]["new_confirmed"]), \
            int(corona_data[i]["total_deaths"]), \
            int(corona_data[i]["new_deaths"]), \
            int(corona_data[i]["total_recovered"]), \
            int(corona_data[i]["new_recovered"]), \
            float(corona_data[i]["fatality"]), \
            float(corona_data[i]["recovery"]), \
            float(corona_data[i]["incidence"])))

        conn.commit()
        conn.close()
        print("corona_data table update complete")

    # 기능 3. 외교부 api 호출, 주기 : 50초
    def update_Api_Data(self):
        # 0. 쓰레드 실행
        threading.Timer(50, self.update_Api_Data).start()

        # 1. api 호출
        # text_data columns : ['country_iso_alp2', 'country_name', 'notice', 'alarm_lvl']
        text_data = self.__get_text_api()
        # level_data columns : ['country_eng_nm', 'country_iso_alp2', 'country_nm', 'alarm_lvl']
        get_level_data = self.__get_level_api()

        # 2. 중복 나라 제거
        iso_list = []
        level_data = []
        for i in range(len(get_level_data)):
            if get_level_data[i]["country_iso_alp2"] in iso_list:
                continue
            iso_list.append(get_level_data[i]["country_iso_alp2"])
            level_data.append(get_level_data[i])
        
        # 3. api 데이터 병합
        dict_list = []
        for r in level_data: 
            country_kr = r["country_nm"]
            if r['alarm_lvl'] == None:
                r['alarm_lvl'] = -1
            key = r['country_iso_alp2']
            value = r['alarm_lvl']
            name = r["country_eng_nm"]
            dict_list.append({'country_name' : name, 'country_iso_alp2' : key, 'alarm_lvl' : value, "country_kr" : country_kr})

        for i in dict_list:
            i["notice"] = "없음"
            for j in text_data:
                if i['country_iso_alp2'] == j['country_iso_alp2']:
                    i["notice"] = j["notice"].replace("'", "`").replace('"', "`") # 따옴표들 백틱으로 변경

        # 4. db 연결
        conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE api_data') # 테이블 레코드 비우기
        
        # 5. 해당 테이블에 데이터 추가
        for i in range(len(dict_list)):
            cur.execute('INSERT INTO api_data VALUES("{0}", "{1}", "{2}", "{3}", "{4}")'.format(\
            dict_list[i]["country_name"], \
            dict_list[i]["country_iso_alp2"], \
            dict_list[i]["country_kr"], \
            float(dict_list[i]["alarm_lvl"]),\
            dict_list[i]["notice"]))
            # "text_data[i]["notice"] <- "asdsadfasfb" 대신 추가 해야함 11/16

        conn.commit()
        conn.close()
        print("api_data table update complete")








    # 1-1 vaccine data scraping
    def __get_vaccine_scraping(self):
        year = datetime.datetime.now().year

        driver = webdriver.Chrome(r'.\chromedriver.exe')
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

    # 2-1 coronaboard scraping
    def __get_corona_scraping(self):
        # coronaboard 관련 스크래핑 코드 -> return : board_dict
        
        board_dict = []  # 국가별 코로나 정보를 저장할 리스트

        # 웹사이트 실행
        driver = webdriver.Chrome(r'.\chromedriver.exe')
        driver.implicitly_wait(5)

        driver.get('https://coronaboard.kr/en')
        time.sleep(2)

        for i in range(2):
            #some_element까지 스크롤
            some_element = driver.find_element_by_xpath('//*[@id="global-slide"]/div/div[3]/p/a')
            action = ActionChains(driver)
            action.move_to_element(some_element).perform()
            time.sleep(1)

            #더보기 클릭
            more_data = driver.find_element_by_xpath('//*[@id="show-more"]')
            more_data.click()
            time.sleep(1)

        # table 읽기
        table = driver.find_element_by_tag_name('tbody')
        tr = table.find_elements_by_tag_name('tr')

        # 나라별 결과 나누기
        result = []
        for t in tr:
            info = t.text
            result.append(info)

        for r in result:
            data = r.split('\n')
            if len(data) == 4:
                a = data[0]     # index, country_name, total_confirmed
                b = data[1]     # new_confirmed, total_deaths
                c = data[2]     # new_deaths, total_recovered
                d = data[3]     # new_recovered, fatality, recovery, incidence
            else:
                a = data[0]     # index, country_name, total_confirmed
                b = data[1]     # new_confirmed, total_deaths
                c = "N/A"       # new_deaths, total_recovered
                d = data[2]     # new_recovered, fatality, recovery, incidence


            # 데이터 컬럼별로 나누기 (a)
            try:
                country_name = re.search('([A-Za-z]+[.]?[\s]?)+', a).group()
                total_confirmed = re.search('[\d+,?]+\d{3}$', a).group()
            except:
                total_confirmed = a.split(' ')[-1]   # 정규식으로 걸러지지 않은 값

            # 데이터 컬럼별로 나누기 (b와 c)
            if b.startswith('('):
                new_confirmed, total_deaths  = b.split(" ")
            else:
                new_confirmed, total_deaths = 'N/A', b

            if c.startswith('('):
                new_deaths, total_recovered = c.split(" ")
            else:
                new_deaths, total_recovered = 'N/A', c

            # 데이터 컬럼별로 나누기 (d) ---> 경우의 수 3개
            d_list = d.split()
            if len(d_list) == 3:
                fatality, recovery, incidence = d.split(" ")
            elif len(d_list) == 4:
                new_recovered, fatality, recovery, incidence = d.split()
            else:
                new_deaths, new_recovered, fatality, recovery, incidence = d.split()

            # 데이터 형변환 및 결측값 처리
            try: total_confirmed = int(total_confirmed.replace(',', ''))  # , 제거 후 int로 변환
            except: total_confirmed = -1

            try: new_confirmed = int(new_confirmed[2:-1].replace(',', ''))  # new_confirmed값이 있는경우 (+)삭제하고 int 변환
            except: new_confirmed = -1

            try: total_deaths = int(total_deaths.replace(',', ''))  # total_deaths값 int로 변환
            except: total_deaths = -1

            try: new_deaths = int(new_deaths[2:-1].replace(',', ''))  # new_confirmed값이 있는경우 (+)삭제하고 int 변환
            except: new_deaths = -1

            try: total_recovered = int(total_recovered.replace(',', ''))  # total_recovered값 int 변환
            except: total_recovered = -1

            try : new_recovered = int(new_recovered[2:-1].replace(',', '')) # new_recovered값 int 변환
            except: new_recovered = -1

            try : fatality = float(fatality)
            except: fatality = -1

            try: recovery = float(recovery)
            except: recovery = -1

            try: incidence = int(incidence.replace(',',''))
            except: incidence = -1

            data = {
                'country_name' : country_name,
                'total_confirmed' : total_confirmed,
                'new_confirmed' : new_confirmed,
                'total_deaths' : total_deaths,
                'new_deaths' : new_deaths,
                'total_recovered' : total_recovered,
                'new_recovered' : new_recovered,
                'fatality' : fatality,
                'recovery' : recovery,
                'incidence': incidence
            }
            board_dict.append(data)
            
        # with open ('./covid_info.json', 'w') as f:
        #     json.dump(board_dict, f)

        return board_dict



    # 3-1 notice data api 
    def __get_text_api(self):
        # text 가져오기
        url = 'http://apis.data.go.kr/1262000/CountryOverseasArrivalsService/getCountryOverseasArrivalsList'
        params ={
            'serviceKey' : "Sk4Syk+ddhdzDzSKdby8eRCdDfe912d+TxPmhp7Uq2UoxKrXMqgSQDv1vLQsOknyyNqHVICzTmwubry2uL7vig==",
            'pageNo': 1,
            'numOfRows': 200
        }
        
        response = requests.get(url, params=params)
        response_text_dict = eval(response.text)
        data_text = response_text_dict['data']
        
        for er in data_text:    
            er['country_name'] = er.pop('country_eng_nm')
            er['notice'] = er.pop("wrt_dt") + "\r\n" + er.pop('txt_origin_cn')
            er.pop('country_nm')
            er.pop('html_origin_cn')
            er.pop('notice_id')
            er.pop('title')
        
        return data_text

    # 3-2 caution data api
    def __get_level_api(self):
        # 경보 가져오기
        url = 'http://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2'
        params ={'serviceKey' : 'l2Tz12aLRivDhn4CKg0XE5RGdY4wc7asf9UaKQmF6ZRiigW0klMF5ioFkBI47WiY0XTahwpsqMYX1l9Kl6gaWg==',
                'returnType' : 'JSON',
                'numOfRows' : '200',
                'pageNo' : '1' }

        response = requests.get(url, params=params)
        result =response.json()
        data_level = result['data']

        return data_level