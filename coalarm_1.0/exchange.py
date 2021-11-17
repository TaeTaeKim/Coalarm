
# Latest update
# 11/17 환율 데이터를 db에서 읽어옴

# 환율 API를 이용해서 반환하는 함수.
import requests
import pymysql

def exchange(ISO):
    conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from exchange_data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    
    cur.execute("select * from exchange_data where cur_unit = 'USD'")
    dollar = cur.fetchall()[0]
    conn.close()

    EU = [
        "GG", "JE", "AX", "EE", "FI", "FO", "IE", "IM", "IS", "LT", "LV", "SJ",
        "AT", "BE", "DE", "DD", "FR", "FX", "LI", "LU", "MC", "NL", "BG", "BY", "CZ", "HU", "MD", 
        "PL", "RO", "RU", "SU", "SK", "UA", "AD", "AL", "BA", "ES", "GI", "GR", "HR", "IT", "ME", "MK", 
        "MT", "RS", "PT", "SI", "SM", "VA", "YU"
        ]
        
    if ISO in EU:
        for d in response_text_dict:
            if d['cur_unit'] =='EUR':
                return [d['deal_bas_r'],d['cur_nm']]
 
    for i in response_text_dict:
        if ISO==i['cur_unit'][:2]:
            exchange_rate = i['deal_bas_r']
            exchange_name = i['cur_nm']
            return [exchange_rate,exchange_name]

    return [dollar[2],dollar[0]]