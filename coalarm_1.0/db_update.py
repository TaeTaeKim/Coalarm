
# Latest update
# 11/17 내부 호출 method를 외부 파일로 분리 (corona_vaccine_data_scraping.py, corona_data_scraping.py, corona_api.py)
# 내용 : __(private) 제거, 내부 호출(self) 제거, 
# 장점 : import 간소화, 코드 리딩이 보다 쉬워짐.
# 단점 : private을 표현할 수 없음.

import pymysql
import threading
import json

# 코로나 백신 데이터 가져오기
from corona_vaccine_data_scraping import get_vaccine_scraping
# 코로나 데이터 가져오기
from corona_data_scraping import get_corona_scraping
# 코로나 관련 api 가져오기
from corona_api import get_level_api, get_text_api, get_exchange_api
# 대사관 데이터 가져오기
from embassy_data import get_embassy_data

class AsyncTask:

    def __init__(self):
        print("background thread - db update")

    # 기능 1. scraping vaccine data update, 주기 : 100초
    def update_Corona_Vaccine_Data(self):
        
        # 0. 쓰레드 실행
        threading.Timer(100, self.update_Corona_Vaccine_Data).start()
        
        # 1. scraping
        vaccine_data = get_vaccine_scraping() 

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
        get_corona_data = get_corona_scraping()

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

    # 기능 3. 공지사항, 경보 api, 환율 api  호출, 주기 : 60초
    def update_Api_Data(self):
        
        # 0. 쓰레드 실행
        threading.Timer(60, self.update_Api_Data).start()
        
        # api data
        # 1. api 호출
        text_data = get_text_api()
        get_level_data = get_level_api()

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

        conn.commit()
        conn.close()

        print("api_data table update complete")   
        
        # exchange_data
        # 1. api 호출
        exchange_data = get_exchange_api()
        
        if len(exchange_data) != 0:
            # 2. db 연결
            conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
            cur = conn.cursor()
            cur.execute('TRUNCATE TABLE exchange_data') # 테이블 레코드 비우기
            
            # 3. 해당 테이블에 데이터 추가
            for i in range(len(exchange_data)):
                cur.execute('INSERT INTO exchange_data VALUES("{0}", "{1}", "{2}")'.format(\
                exchange_data[i]["cur_nm"], \
                exchange_data[i]["cur_unit"], \
                exchange_data[i]["deal_bas_r"]))

            conn.commit()
            conn.close()

            print("exchange table update complete")
        else:
            print("주말엔 exchange api가 안와요")