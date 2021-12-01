
# Latest update
# 11/17 내부 호출 method를 외부 파일로 분리 (corona_vaccine_data_scraping.py, corona_data_scraping.py, corona_api.py)
# 내용 : __(private) 제거, 내부 호출(self) 제거, 
# 장점 : import 간소화, 코드 리딩이 보다 쉬워짐.
# 단점 : private을 표현할 수 없음.

import pymysql
import threading
import json
import pandas as pd
import numpy as np

# 코로나 백신 데이터 가져오기
from corona_vaccine_data_scraping import get_vaccine_scraping
# 코로나 데이터 가져오기
from corona_data_scraping import get_corona_scraping
# 코로나 관련 api 가져오기
from corona_api import get_level_api, get_text_api, get_exchange_api
# 대사관 데이터 가져오기
from embassy_data_scraping import get_embassy_data
# 안전 데이터, 범죄 데이터 가져오기
from safety_scraping import get_safety_data
from terror_scraping import get_terror_data
# Safety_Score 데이터 가공 함수
from score import SafetyScore

class AsyncTask:
    
    def __init__(self):
        print("db update - background")

    # 기능 1. corona vaccine data update, 주기 : 24시간
    def update_Corona_Vaccine_Data(self):
        
        # 0. 쓰레드 실행
        t = threading.Timer(500, self.update_Corona_Vaccine_Data)
        t.daemon = True
        t.start()
        
        # 1. scraping
        vaccine_data = get_vaccine_scraping()

        # 2. iso 컬럼 추가
        with open('./json_file/country_ISO.json', 'r') as f:
            iso_list = json.load(f)

        for i in range(len(vaccine_data)):
            vaccine_data[i]["iso_code"] = vaccine_data[i]["country"]
            for j in range(len(iso_list)):
                if vaccine_data[i]["country"] == iso_list[j]["Name"]:
                    vaccine_data[i]["iso_code"] = iso_list[j]["Code"]

        # 3. db 연결
        conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Corona_Vaccine_Data') # 테이블 레코드 비우기

        # 4. 해당 테이블에 데이터 추가
        for i in range(len(vaccine_data)):
            cur.execute('INSERT INTO Corona_Vaccine_Data VALUES("{0}", "{1}", "{2}", "{3}")'.format(\
            vaccine_data[i]["country"], \
            vaccine_data[i]["iso_code"], \
            float(vaccine_data[i]["partly"]),\
            float(vaccine_data[i]["fully"])))
        conn.commit()
        conn.close()
        print("corona_vaccine_date table update complete")

    # 기능 2. corona data update, 주기 : 1시간
    def update_Corona_Data(self):

        # 0. 쓰레드 실행
        t = threading.Timer(400, self.update_Corona_Data)
        t.daemon = True
        t.start()

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

        for i in range(len(corona_data)):
            corona_data[i]["continent"] = "없음"
            for j in continent:
                if corona_data[i]["country_iso_alp2"] == j["iso_code"]:
                    corona_data[i]["continent"] = j["continent"]

        # 4. db 연결
        conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Corona_Data') # 테이블 레코드 비우기
        
        # 5. 해당 테이블에 데이터 추가
        for i in range(len(corona_data)):
            cur.execute('INSERT INTO Corona_Data VALUES("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}", "{11}")'.format(\
            corona_data[i]["country_name"], \
            corona_data[i]["country_iso_alp2"], \
            corona_data[i]["continent"], \
            int(corona_data[i]["total_confirmed"]), \
            int(corona_data[i]["new_confirmed"]), \
            int(corona_data[i]["total_deaths"]), \
            int(corona_data[i]["new_deaths"]), \
            int(corona_data[i]["total_recovered"]), \
            int(corona_data[i]["new_recovered"]), \
            float(corona_data[i]["recovery"]), \
            float(corona_data[i]["fatality"]), \
            float(corona_data[i]["incidence"])))

        conn.commit()
        conn.close()
        print("corona_data table update complete")

    # 기능 3. api date update, 주기 : 24시간
    def update_Api_Data(self):
        
        # 0. 쓰레드 실행
        t = threading.Timer(300, self.update_Api_Data)
        t.daemon = True
        t.start()
        
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
            level_data.append(get_level_data[i]) # level_data key : ["country_nm", "alarm_lvl", "country_iso_alp2", "country_eng_nm"]
        
        # 3. 기반 데이터(country_kr_ISO.json)에 api 데이터 병합
        with open('./json_file/country_kr_ISO.json', 'r') as f:
            json_country_kr = json.load(f)  # json_country_kr key : ["country_kr", "iso_code"]

        dict_list = []

        for i in json_country_kr:
            i["alarm_lvl"] = -1
            i["country_eng_nm"] = "없음"
            for r in level_data:
                if i["iso_code"] == r["country_iso_alp2"]:
                    if r['alarm_lvl'] == None:
                        i['alarm_lvl'] = 5
                    else:
                        i["alarm_lvl"] = r["alarm_lvl"]
                    i["country_eng_nm"] = r["country_eng_nm"]
            dict_list.append({'country_name' : i["country_eng_nm"], 'country_iso_alp2' : i["iso_code"], \
                              'alarm_lvl' : i["alarm_lvl"], "country_kr" : i["country_kr"]})

        for i in dict_list:
            i["notice"] = None
            for j in text_data:
                if i['country_iso_alp2'] == j['country_iso_alp2']:
                    i["notice"] = j["notice"].replace("'", "`").replace('"', "`") # 따옴표들 백틱으로 변경

        # 4. db 연결
        conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")  
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Api_Data') # 테이블 레코드 비우기
        
        # 5. 해당 테이블에 데이터 추가
        for i in range(len(dict_list)):
            cur.execute('INSERT INTO Api_Data VALUES("{0}", "{1}", "{2}", "{3}", "{4}")'.format(\
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
            conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
            cur = conn.cursor()
            cur.execute('TRUNCATE TABLE Exchange_Data') # 테이블 레코드 비우기
            
            # 3. 해당 테이블에 데이터 추가
            for i in range(len(exchange_data)):
                cur.execute('INSERT INTO Exchange_Data VALUES("{0}", "{1}", "{2}")'.format(\
                exchange_data[i]["cur_nm"], \
                exchange_data[i]["cur_unit"], \
                exchange_data[i]["deal_bas_r"]))

            conn.commit()
            conn.close()

            print("exchange table update complete")
        else:
            print("주말엔 exchange api가 안와요")

    # 기능 4. embassy data update, 주기 : 24시간
    def update_Embassy_Data(self):

        # 0. 쓰레드 실행
        t = threading.Timer(200, self.update_Embassy_Data)
        t.daemon = True
        t.start()

        # 1. scraping
        embassy_data = get_embassy_data()
        # return column : ['country_eng_nm', 'country_iso_alp2', 'country_nm', 'embassy_kor_nm', 'url']

        # 3. db 연결
        conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Embassy_Data') # 테이블 레코드 비우기

        # 4. 해당 테이블에 데이터 추가
        for i in range(len(embassy_data)):
            cur.execute('INSERT INTO Embassy_Data VALUES("{0}", "{1}", "{2}")'.format(\
            embassy_data[i]["country_iso_alp2"], \
            embassy_data[i]["embassy_kor_nm"], \
            embassy_data[i]["url"]))
        conn.commit()
        conn.close()
        print("embassy_data table update complete")

    # 기능 5. safety data update, 주기 : 24시간
    def update_Safety_Data(self):
        
        # 0. 쓰레드 실행
        t = threading.Timer(600, self.update_Safety_Data)
        t.daemon = True
        t.start()

        # 1. scraping
        safety_data = get_safety_data() # return : ['Country', 'Safety_index', 'Numbeo_index', 'Homicide_rate']
        terror_data = get_terror_data() # return : ['Ranking', 'Country', 'Last', 'Previous']

        # 2. 기반 데이터(country_ISO.json)에 api 데이터 병합
        with open('./json_file/country_ISO.json', 'r') as f:
            country_iso = json.load(f)  # json_country key : ["Code", "Name"]

        for i in safety_data:
            i["iso_code"] = "없음"
            for j in country_iso:
                if i["Country"] == j["Name"]:
                    i["iso_code"] = j["Code"]
        
        for i in terror_data:
            i["iso_code"] = "없음"
            for j in country_iso:
                if i["Country"] == j["Name"]:
                    i["iso_code"] = j["Code"]
        
        df_safety_data = pd.DataFrame(safety_data)
        df_terror_data = pd.DataFrame(terror_data)

        data = pd.merge(df_safety_data, df_terror_data, how = 'outer', on = "iso_code").fillna(-1)
        data = data.to_dict(orient = "records") 
        # return : {'Safety_index', 'Numbeo_index', 'Homicide_rate', 'iso_code', 'Last', 'Previous'}
        
        # 3. db 연결
        conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Safety_Data') # 테이블 레코드 비우기

        # 4. 해당 테이블에 데이터 추가
        for i in range(len(data)):
            cur.execute('INSERT INTO Safety_Data VALUES("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(\
            data[i]["iso_code"], \
            float(data[i]["Safety_index"]),\
            float(data[i]["Numbeo_index"]),\
            float(data[i]["Homicide_rate"]),\
            float(data[i]["Last"]),\
            float(data[i]["Previous"])))

        conn.commit()
        conn.close()
        print("safety_data table update complete")

    # 기능 6. Safety_Score update, 주기 : 24시간
    def update_Safety_Score(self):
        
        # 0. 쓰레드 실행
        t = threading.Timer(500, self.update_Corona_Vaccine_Data)
        t.daemon = True
        t.start()

        # 1. 기반 데이터 호출
        with open('./json_file/new_continent.json', 'r') as f:
            df_continent = pd.DataFrame(json.load(f))  # json_country key : ["iso_code", "continent"]
        with open('./json_file/country_kr_ISO.json', 'r') as f:
            json_country_kr = json.load(f)  # json_country_kr key : ["country_kr", "iso_code"]

        # 2. db 연결
        conn = pymysql.connect(host='localhost', user="coalarm", password="coalarm", db="coalarm", charset="utf8")
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE Safety_Score') # 테이블 레코드 비우기
        '''
        필요한 input 값
        [
            {
                'iso_code': (value),
                'total_caeses_per_1million_population' : (value),
                'recovered': (value),
                'critical': (value),
                'fully_vaccinated': (value),
                'lvl': (value),
                'homicide_rate': (value),
                'safety_index': (value),
                'numbeo_index': (value),
                'last_terrorism': (value),
                'previous_terrorism': (value),
            },
            ...
        ]
        (value)가 nan, -1 인 값은 대륙(서유럽 등의 소분류) 평균 적용
        이후에도 (value)가 nan, -1 인 값은 전 세계 평균 적용 
        '''
        # 3. db 데이터 꺼내와서 가공
        cur.execute("select v.iso_code, v.fully_vaccinated, s.homicide_rate, a.caution, c.total_caeses_per_1million_population, c.recovered_ratio, c.critical_ratio \
        from Corona_Vaccine_Data v \
        join Safety_Data s using(iso_code) \
        join Api_Data a using(iso_code) \
        join Corona_Data c using(iso_code)")
        row_headers=[x[0] for x in cur.description]
        rv = cur.fetchall()
        recommend_data=[]
        for result in rv:
            recommend_data.append(dict(zip(row_headers,result)))

        df_recommend_data = pd.DataFrame(recommend_data).replace(-1, np.NaN)
        df_recommend_data["caution"] = df_recommend_data["caution"].apply(lambda x : x if x != 5 else 1.5)
        df_recommend_data = pd.merge(df_continent, df_recommend_data, how = 'left', on = "iso_code").groupby("continent").apply(lambda x: x.fillna(x.mean()))
        df_recommend_data = df_recommend_data.drop(["continent"], axis=1).reset_index()
        # df_recommend_data = df_recommend_data.dropna(axis=0)
        df_recommend_data = df_recommend_data.fillna(df_recommend_data.mean())
        df_recommend_data = df_recommend_data.to_dict(orient = "records")
        #print(len(df_recommend_data), type(df_recommend_data))

        df_score = SafetyScore(df_recommend_data)
        '''
        [
            {},
            ...
            {}
        ]
        형태로 변환
        '''
        score = []
        for i in range(len(df_score)):
            dict_score = {}
            dict_score['iso_code'] = df_score['iso_code'][i]
            dict_score['score'] = df_score['score'][i]
            dict_score["country_kr"] = dict_score["iso_code"]
            for j in json_country_kr:
                if dict_score["iso_code"] == j["iso_code"]:
                    dict_score["country_kr"] = j["country_kr"]
            score.append(dict_score)

        # 4. 해당 테이블에 데이터 추가        
        for i in range(len(score)):
            cur.execute("INSERT INTO Safety_Score VALUES('{0}', '{1}', '{2}')".format(\
                score[i]["iso_code"], \
                score[i]["country_kr"], \
                float(score[i]["score"])))
        conn.commit()
        conn.close()
        print("Safety Score table update complete")

