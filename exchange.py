# 환율 API를 이용해서 반환하는 함수.
import requests
def exchange(ISO):
    url  = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': 'y6VrwVGHQWHtS19rOIvBg7SJTi1O115y',
        'data': 'AP01'
    }
    EU = [
        "GG", "JE", "AX", "EE", "FI", "FO", "IE", "IM", "IS", "LT", "LV", "SJ",
        "AT", "BE", "DE", "DD", "FR", "FX", "LI", "LU", "MC", "NL", "BG", "BY", "CZ", "HU", "MD", 
        "PL", "RO", "RU", "SU", "SK", "UA", "AD", "AL", "BA", "ES", "GI", "GR", "HR", "IT", "ME", "MK", 
        "MT", "RS", "PT", "SI", "SM", "VA", "YU"
        ]
    response = requests.get(url, params=params)
    
    response_text_dict = response.json()
    dollar = response_text_dict[-1]['deal_bas_r']
    if ISO in EU:
        for d in response_text_dict:
            if d['cur_unit'] =='EUR':
                return [d['deal_bas_r'],d['cur_nm']]
        
    for i in response_text_dict:
        if ISO==i['cur_unit'][:2]:
            exchange_rate = i['deal_bas_r']
            exchange_name = i['cur_nm']
            return [exchange_rate,exchange_name]

    return [dollar,response_text_dict[-1]['cur_nm']]