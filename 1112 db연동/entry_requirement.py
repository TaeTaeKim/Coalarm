
# https://www.data.go.kr/data/15085787/openapi.do


import requests
import sqlite3
import threading
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

class AsyncTask:

    def __init__(self):
        conn = sqlite3.connect('database.db')
        print ("Opened database successfully")
        
        # drop table
        conn.execute("DROP TABLE Corona_Vaccine_Data")
        # create table 
        conn.execute('CREATE TABLE IF NOT EXISTS Corona_Data ( \
            country TEXT, \
            iso_code TEXT, \
            total_cases INT, \
            new_cases INT, \
            total_deaths INT, \
            new_deaths INT, \
            total_recovered INT, \
            new_recovered INT, \
            recovered_ratio REAL, \
            critical REAL, \
            total_caeses_per_1million_population REAL, \
            population INT, \
            caution INT, \
            notice TEXT)')
# 3~5번 TEXT -> REAL
        conn.execute('CREATE TABLE IF NOT EXISTS Corona_Vaccine_Data ( \
            country TEXT, \
            iso_code TEXT, \
            vaccinated TEXT, \
            fully_vaccinated TEXT, \
            additional_dose TEXT)')
        print ("Table created  successfully")
        conn.close()


    # 기능 1 
    def update_Corona_Vaccine_Data(self):   # 백신 데이터 주기 50, ISO - 없음
        threading.Timer(50, self.update_Corona_Vaccine_Data).start()
        vaccine_data = self.__get_vaccine_scraping()
        conn = sqlite3.connect('database.db')
        # print ("Opened database successfully")
        
        with open('./json_file/country_ISO.json', 'r') as f:
            iso_list = json.load(f)
        for i in range(len(vaccine_data)):
            vaccine_data[i]["iso_code"] = "없는애들 채우기"
            for j in range(len(iso_list)):
                if vaccine_data[i]["country"] == iso_list[j]["Name"]:
                    vaccine_data[i]["iso_code"] = iso_list[j]["Code"]
        # 3~5번 float 잠깐 뺌
        for i in range(len(vaccine_data)):
            conn.execute("INSERT INTO Corona_Vaccine_Data VALUES('{0}', '{1}', '{2}','{3}','{4}')".format(\
            vaccine_data[i]["country"], \
            vaccine_data[i]["iso_code"], \
            vaccine_data[i]["vaccinated"], \
            vaccine_data[i]["fully_vaccinated"], \
            vaccine_data[i]["additional_dose"]))
        # 3~5번 float 잠깐 뺌

        conn.commit()
        conn.close()
        print("vaccine db update complete")

    # 기능 2
    def update_Corona_Data(self):    # 주기 : 50, ISO - 있음
        threading.Timer(50, self.update_Corona_Data).start()
        # 데이터 호출 -> Corona_Data db에 저장
        text_data = self.__get_text_api()   # 정보 데이터 호출
        level_data = self.__get_level_api() # 경보 데이터 호출

        # 취합 
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
        file_path = "./json_file/corona.json"
        with open(file_path, 'w') as f:
            json.dump(data_text, f)
        print("api 호출 완료")


        #----------------- 임시 저장 ---------------------
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
        
        with open('./json_file/country_ISO.json', 'r') as f:
            b = json.load(f)
        
        for i in range(len(data)-3):
            data[i]['country_iso_alp2'] = "없음"
            for j in b:
                if data[i]['country_name'] == j['Name']:
                    data[i]['country_iso_alp2'] = j['Code']
            if data[i]['country_iso_alp2'] == "없음":
                data.pop(i)

        # 저장
        file_path = "./json_file/sample_data.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print("데이터 스크래핑 완료")

    def __get_text_api(self):
        # text 가져오기, return : 
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
        
        return data_text

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

    def __get_vaccine_scraping(self):

        #아이디
        id = "infamousgames@hanmail.net"
        #비밀번호
        pw = "aa1313aa"  

        driver = webdriver.Chrome(r'.\chromedriver.exe')
        driver.set_window_position(0, 0)
        driver.set_window_size(3000, 3000)
        driver.implicitly_wait(3)

        #메인페이지 접속
        driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
        time.sleep(2)
        # //*[@id="standalone-header"]/div[1]/header/section[1]/div[4]/a[2]/button - 기존
        #메인페이지 login 접속 176 에러 -> async 빼니까 해결
        posting = driver.find_element_by_xpath('//*[@id="standalone-header"]/div[1]/header/section[1]/div[4]/a[2]/button')
        posting.click()
        time.sleep(3)

        #페이스북 로그인 접속
        posting2 = driver.find_element_by_xpath('//*[@id="js-facebook-oauth-login"]')
        posting2.click()
        time.sleep(3)

        #2번째(로그인 팝업창)윈도우 호출
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        #페이스북 로그인
        assert "Facebook" in driver.title 
        login_box = driver.find_element_by_id("email") 
        login_box.send_keys(id) 
        login_box = driver.find_element_by_id("pass") 
        login_box.send_keys(pw)
        login_box.send_keys(Keys.RETURN)
        time.sleep(6)

        #1번째(메인페이지)윈도우 호출
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

        driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
        time.sleep(10)

        #id가 something인 element를 찾음
        some_tag = driver.find_element_by_xpath('//*[@id="covid-signup-module"]/section/div/div[2]/div/button')

        #somthing element까지 스크롤
        action = ActionChains(driver)
        action.move_to_element(some_tag).perform()
        time.sleep(5)

        #show_all 클릭
        posting = driver.find_element_by_xpath('//*[@id="covid-vaccinations-tracker"]/div/div[3]/div[3]/div[1]/div/div[2]')
        posting.click()
        time.sleep(3)

        html = driver.page_source

        #크롤링
        url = "https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html"
        soup = BeautifulSoup(html, "html.parser")
        result = []
        for i in range(1, 188):
            # 국가별 데이터 가져오기
            tag = soup.find(class_ = "g-row-{} svelte-oedzx3".format(i))
            # tag 에서 td 태그들을 선택하기
            td = tag.select('td')
            '''
            td[0].text: country
            td[1].text: vaccinated
            td[2].text: fully_vaccinated
            td[3].text: additional_dose
            '''
            result.append({
                'country': td[0].text,
                'vaccinated': td[1].text.split()[0],
                'fully_vaccinated': td[2].text.split()[0],
                'additional_dose': td[3].text.split()[0]
                })
        return result