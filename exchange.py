# 환율 API를 이용해서 반환하는 함수.
import requests
import json
import pymysql

def exchange(ISO):
    # url  = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    # params = {
    #     'authkey': 'y6VrwVGHQWHtS19rOIvBg7SJTi1O115y',
    #     'data': 'AP01'
    # }
    EU = [
        "GG", "JE", "AX", "EE", "FI", "FO", "IE", "IM", "IS", "LT", "LV", "SJ",
        "AT", "BE", "DE", "DD", "FR", "FX", "LI", "LU", "MC", "NL", "BG", "BY", "CZ", "HU", "MD", 
        "PL", "RO", "RU", "SU", "SK", "UA", "AD", "AL", "BA", "ES", "GI", "GR", "HR", "IT", "ME", "MK", 
        "MT", "RS", "PT", "SI", "SM", "VA", "YU"
        ]
    # response = requests.get(url, params=params)
    
    # response_text_dict = response.json()

    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Exchange_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    # with open('./static/Test_json/exchange.json','r') as f:
    #     response_text_dict = json.load(f)
    for i in range(len(response_text_dict)):
        if response_text_dict[i]["cur_unit"] == "USD":
            dollar = response_text_dict[i]

    if ISO in EU:
        for d in response_text_dict:
            if d['cur_unit'] =='EUR':
                return [d['deal_bas_r'],d['cur_nm']]
        
    for i in response_text_dict:
        if ISO==i['cur_unit'][:2]:
            exchange_rate = i['deal_bas_r']
            exchange_name = i['cur_nm']
            return [exchange_rate,exchange_name]

    return [dollar["cur_unit"],dollar['cur_nm']]
