# import requests
# import json

# url = 'http://apis.data.go.kr/1262000/CountryCovid19SafetyServiceNew/getCountrySafetyNewsListNew'
# params ={
#     'serviceKey' : 'l2Tz12aLRivDhn4CKg0XE5RGdY4wc7asf9UaKQmF6ZRiigW0klMF5ioFkBI47WiY0XTahwpsqMYX1l9Kl6gaWg==',
#     'numOfRows' : '200', 
#     'pageNo' : '1'

# }

# response = requests.get(url, params=params)
# data = str(response.text)
# data = json.loads(data)['data']
# # ['continent_cd', 'continent_eng_nm', 'continent_nm', 'country_eng_nm', 'country_iso_alp2', 'country_nm', 'file_cnt', 
# # 'file_download_url', 'file_path', 'html_origin_cn', 'sfty_notice_id', 'title', 'txt_origin_cn', 'wrt_dt']
# print(data[0]["txt_origin_cn"], type(data[0]), len(data[0]))