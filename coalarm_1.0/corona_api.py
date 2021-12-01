
import requests

# 3-1 exchange data api 
def get_exchange_api():
    url  = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': 'y6VrwVGHQWHtS19rOIvBg7SJTi1O115y',
        'data': 'AP01'
    }
    response = requests.get(url, params=params)
    response_text_dict = response.json()
    return response_text_dict
    # {'result': 1, 'cur_unit': 'AED', 'ttb': '317.93', 'tts': '324.36', 'deal_bas_r': '321.15', 'bkpr': '321', 
    # 'yy_efee_r': '0', 'ten_dd_efee_r': '0', 'kftc_bkpr': '321', 'kftc_deal_bas_r': '321.15', 'cur_nm': '아랍에미리트 디르함'}

# 3-2 notice data api
def get_text_api():
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

# 3-3 caution data api
def get_level_api():
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