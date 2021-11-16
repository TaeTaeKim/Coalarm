import json

# 여기에 DB  data가져오는 query작성.
with open('./static/Test_json/corona_data.json','r') as f:
    coronadata = json.load(f)
with open('./static/Test_json/corona_vaccine_data.json','r') as f:
    vaccinedata = json.load(f)
with open('./static/Test_json/api_data.json','r') as f:
    api_data = json.load(f)

def corona(ISO):
    for data in coronadata:
        if data['country_iso_alp2'] == ISO:
            return data


def vaccine(ISO):
    for data in vaccinedata:
        if data['iso_code'] == ISO:
            return data

def kr_name(ISO):
    for data in api_data:
        if data['country_iso_alp2'] == ISO:
            return data['country_kr']

def notice(ISO):
    for data in api_data:
        data = 'asdf'
        if data['country_iso_alp2'] == ISO:
            noticedata = data['notice'].split('\r\n')
            return