# 환율 API를 이용해서 반환하는 함수.
import pymysql

def exchange(ISO):
    EU = [
        "GG", "JE", "AX", "EE", "FI", "FO", "IE", "IM", "IS", "LT", "LV", "SJ",
        "AT", "BE", "DE", "DD", "FR", "FX", "LI", "LU", "MC", "NL", "BG", "BY", "CZ", "HU", "MD", 
        "PL", "RO", "RU", "SU", "SK", "UA", "AD", "AL", "BA", "ES", "GI", "GR", "HR", "IT", "ME", "MK", 
        "MT", "RS", "PT", "SI", "SM", "VA", "YU"
        ]
    # db select query
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Exchange_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()

    for i in range(len(response_text_dict)):
        if response_text_dict[i]["cur_unit"] == "USD":
            dollar = response_text_dict[i]

    if ISO in EU:
        for d in response_text_dict:
            if d['cur_unit'] =='EUR':
                return [d['deal_bas_r'],d['cur_nm']]
        
    for i in response_text_dict:
        if ISO==i['cur_unit'][:2]:
            if ISO =="JP" or ISO=="ID":
                exchange_rate = float(i['deal_bas_r'].replace(',',""))/100
                exchange_name = i['cur_nm']
                return [str(exchange_rate),exchange_name]
            else:
                exchange_rate = i['deal_bas_r']
                exchange_name = i['cur_nm']
                return [exchange_rate,exchange_name]

    return [dollar["deal_bas_r"],dollar['cur_nm']]
