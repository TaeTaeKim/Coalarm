
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

# 11-15 pymysql - sqlalchemy
from sqlalchemy import create_engine

class AsyncTask:

    def __init__(self):
        # conn = pymysql.connect(host="localhost", user="root", password="root")
        # cur = conn.cursor()
        # print ("Opened database successfully")
        # # drop table
        # # cur.execute("DROP TABLE Corona_Vaccine_Data")
        # # create table 
        # cur.execute('CREATE TABLE IF NOT EXISTS `Corona_Data` (
        #     `id` NOT NULL AUTO_INCREMENT PRIMARY KEY,
        #     `country` VARCHER(50) NOT NULL, \
        #     `iso_code` VARCHER(2) NOT NULL, \
        #     `total_cases` INT NOT NULL, \
        #     `new_cases` INT NOT NULL, \
        #     `total_deaths` INT NOT NULL, \
        #     `new_deaths` INT NOT NULL, \
        #     `total_recovered` INT NOT NULL, \
        #     `new_recovered` INT NOT NULL, \
        #     `recovered_ratio` DECIMAL(3,2) NOT NULL, \
        #     `critical` DECIMAL(3,2) NOT NULL, \
        #     `total_caeses_per_1million_population` DECIMAL(3,2) NOT NULL, \
        #     `population` INT NOT NULL, \
        #     `caution` INT NOT NULL, \
        #     `notice` TEXT NOT NULL)')

        # conn.execute('CREATE TABLE IF NOT EXISTS `Corona_Vaccine_Data` ( \
        #     `id` INT AUTO_INCREMENT, \
        #     `country` VARCHER(50) NOT NULL, \
        #     `iso_code` VARCHER(2) NOT NULL, \
        #     `vaccinated` DECIMAL(3,2) NOT NULL, \
        #     `fully_vaccinated` DECIMAL(3,2) NOT NULL, \
        #     `additional_dose` DECIMAL(3,2) NOT NULL)')
        # print ("Table created  successfully")
        # conn.close()
        pass


    # 기능 1 scraping vaccine data
    def update_Corona_Vaccine_Data(self):   # 백신 데이터 주기 24시간, ISO - 없음
        # threading.Timer(100, self.update_Corona_Vaccine_Data).start()
        vaccine_data = self.__get_vaccine_scraping()
        conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
        cur = conn.cursor()
        # print ("Opened database successfully")
        
        # for i in range(len(vaccine_data)):
        #     print(vaccine_data[i])

        with open('./json_file/country_ISO.json', 'r') as f:
            iso_list = json.load(f)
        # print(vaccine_data[0].keys())
        for i in range(len(vaccine_data)):
            vaccine_data[i]["iso_code"] = "없음"+str(i)
            for j in range(len(iso_list)):
                if vaccine_data[i]["country"] == iso_list[j]["Name"]:
                    vaccine_data[i]["iso_code"] = iso_list[j]["Code"]

        print(vaccine_data)

        for i in range(len(vaccine_data)):

            cur.execute('INSERT INTO corona_vaccine_data VALUES("{0}", "{1}", "{2}", "{3}")'.format(\
            vaccine_data[i]["country"], \
            vaccine_data[i]["iso_code"], \
            float(vaccine_data[i]["partly"]),\
            float(vaccine_data[i]["fully"])))

        conn.commit()
        conn.close()
        print("vaccine db update complete")
    # 기능 3 call_api
    def update_Api_Data(self):
        threading.Timer(50, self.update_Api_Data).start()
        text_data = self.__get_text_api()   # 정보 데이터 호출
        level_data = self.__get_level_api() # 경보 데이터 호출

        # 취합 
        dict_list = []
        for r in level_data:
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
        print("api update complate")

    # 기능 2    coronaboard scraping
    def update_Corona_Data(self):    # 주기 : 2시간, ISO - 없음
        threading.Timer(50, self.update_Corona_Data).start()
        # 데이터 호출 -> Corona_Data db에 저장
        # text_data = self.__get_text_api()   # 정보 데이터 호출
        # level_data = self.__get_level_api() # 경보 데이터 호출

        # # 취합 
        # dict_list = []
        # for r in level_data:
        #     if r['alarm_lvl'] != None:
        #         key = r['country_iso_alp2']
        #         value = r['alarm_lvl']
        #         dict_list.append({'country_iso_alp2' : key, 'alarm_lvl' : value})

        # #data_text : 'text', dict_list : 'alarm_lvl'  , join : 'country_iso_alp2'
        # for i in data_text:
        #     i["alarm_lvl"] = "위험"
        #     for j in dict_list:
        #         if i['country_iso_alp2'] == j['country_iso_alp2']:
        #             i["alarm_lvl"] = j["alarm_lvl"]

        # # 저장
        # file_path = "./json_file/corona.json"
        # with open(file_path, 'w') as f:
        #     json.dump(data_text, f)
        # print("api 호출 완료")


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

        # #아이디
        # id = "infamousgames@hanmail.net"
        # #비밀번호
        # pw = "aa1313aa"

        # driver = webdriver.Chrome(r'.\chromedriver.exe')
        # driver.set_window_position(0, 0)
        # driver.set_window_size(3000, 3000)
        # driver.implicitly_wait(3)

        # #메인페이지 접속
        # driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
        # time.sleep(2)

        # posting = driver.find_element_by_xpath('//*[@id="standalone-header"]/div[1]/header/section[1]/div[4]/a[2]/button')
        # posting.click()
        # time.sleep(1)

        # #페이스북 로그인 접속
        # posting2 = driver.find_element_by_xpath('//*[@id="js-facebook-oauth-login"]')
        # posting2.click()
        # time.sleep(3)

        # #2번째(로그인 팝업창)윈도우 호출
        # driver.switch_to.window(driver.window_handles[1])
        # time.sleep(1)

        # #페이스북 로그인
        # assert "Facebook" in driver.title 
        # login_box = driver.find_element_by_id("email") 
        # login_box.send_keys(id)
        # login_box = driver.find_element_by_id("pass") 
        # login_box.send_keys(pw)
        # login_box.send_keys(Keys.RETURN)
        # time.sleep(6)

        # #1번째(메인페이지)윈도우 호출
        # driver.switch_to.window(driver.window_handles[0])
        # time.sleep(1)

        # driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
        # time.sleep(10)

        # #id가 something인 element를 찾음
        # some_tag = driver.find_element_by_xpath('//*[@id="covid-signup-module"]/section/div/div[2]/div/button')

        # #somthing element까지 스크롤
        # action = ActionChains(driver)
        # action.move_to_element(some_tag).perform()
        # time.sleep(5)

        # #show_all 클릭
        # posting = driver.find_element_by_xpath('//*[@id="covid-vaccinations-tracker"]/div/div[3]/div[3]/div[1]/div/div[2]')
        # posting.click()
        # time.sleep(3)

        # html = driver.page_source

        # #크롤링
        # url = "https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html"
        # soup = BeautifulSoup(html, "html.parser")
        # result = []
        # for i in range(1, 188):
        #     # 국가별 데이터 가져오기
        #     # class가 자주 바뀜 : g-row-{} svelte-ns1nch, g-row-{} svelte-oedzx3
        #     tag = soup.find(class_ = "g-row-{} svelte-ns1nch".format(i))
        #     # tag 에서 td 태그들을 선택하기
        #     td = tag.select('td')
        #     '''
        #     td[0].text: country
        #     td[1].text: vaccinated
        #     td[2].text: fully_vaccinated
        #     td[3].text: additional_dose
        #     '''
            
        #     result.append({
        #         'country': td[0].text,
        #         'vaccinated': td[1].text.split()[0],
        #         'fully_vaccinated': td[2].text.split()[0],
        #         'additional_dose': td[3].text.split()[0]
        #         })
        # return result

        year = datetime.datetime.now().year

        driver = webdriver.Chrome(r'.\chromedriver.exe')
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

        soup = BeautifulSoup(html, "html.parser")
        vaccine_dict = {}
        vaccine_datas = []
        # vaccine_columns = ['country', 'fully', 'partly']
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