import json

# 여기에 DB  data가져오는 query작성.
with open('./static/Test_json/corona_data.json','r') as f:
    coronadata = json.load(f)
with open('./static/Test_json/corona_vaccine_data.json','r') as f:
    vaccinedata = json.load(f)
with open('./static/Test_json/api_data.json','r') as f:
    api_data = json.load(f)
inbound = ["목적", "외국인", "한국", "해외입국자","금지", "허용", "중단","허가","허용","불허","제한","통제","폐쇄","불가","관광","중지","통제"]
document = ["확인서", "허가증", "신고서", "서약서","온라인","결과서","PCR","검사","카드","보험","증명서","QR","디지털","필수","결과지","서류","검진서","검사서","공인서"]
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
    inbound_notice = []
    document_notice = []
    isolate_notice =[]
    visa_notice =[]
    
    for data in api_data:
        if data['country_iso_alp2'] == ISO:
            # 선택된 나라의 notice를 가져옴
            noticedata = data['notice'].split('\r\n')
            for phrase in noticedata:
                for i in inbound:
                    if i in phrase and (phrase.startswith('※') or phrase.startswith('▸')):
                        inbound_notice.append(phrase)
                for i in document:
                    if i in phrase and (phrase.startswith('※') or phrase.startswith('▸')):
                        document_notice.append(phrase)
                if '격리' in phrase:
                    isolate_notice.append(phrase)
                if '비자' in phrase:
                    visa_notice.append(phrase)
    notice = {"inbound":set(inbound_notice),'document':set(document_notice),'isolate':set(isolate_notice),'visa':set(visa_notice)}
    return notice

def noticeall(ISO):
    for data in api_data:
        if data['country_iso_alp2'] == ISO:
            allnotice = data['notice'].split('\r\n')
            return allnotice