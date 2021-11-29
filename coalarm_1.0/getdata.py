
# Latest update
# 11/17 json 파일 -> db 교체 완료 

import json
import pymysql

# import user_info
# coalarm = user_info.user_info

conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
cur = conn.cursor()

cur.execute("select * from Corona_Data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
coronadata=[]
for result in rv:
    coronadata.append(dict(zip(row_headers,result)))

cur.execute("select * from Corona_Vaccine_Data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
vaccinedata=[]
for result in rv:
    vaccinedata.append(dict(zip(row_headers,result)))

cur.execute("select * from Api_Data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
api_data=[]
for result in rv:
    api_data.append(dict(zip(row_headers,result)))

conn.close()

inbound = ["목적", "외국인", "한국", "해외입국자","금지", "허용", "중단","허가","허용","불허","제한","통제","폐쇄","불가","관광","중지","통제"]
document = ["확인서", "허가증", "신고서", "서약서","온라인","결과서","PCR","검사","카드","보험","증명서","QR","디지털","필수","결과지","서류","검진서","검사서","공인서"]
def corona(ISO):
    # data = query() : 딕셔너리
    for data in coronadata:
        if data['iso_code'] == ISO:
            return data


def vaccine(ISO):
    for data in vaccinedata:
        if data['iso_code'] == ISO:
            return data

def kr_name(ISO):
    for data in api_data:
        if data['iso_code'] == ISO:
            return data['country_kr']

def notice(ISO):
    inbound_notice = []
    document_notice = []
    isolate_notice =[]
    visa_notice =[]
    
    for data in api_data:
        if data['iso_code'] == ISO:
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
    notice = {"inbound":list(set(inbound_notice)),'document':list(set(document_notice)),'isolate':list(set(isolate_notice)),'visa':list(set(visa_notice))}
    return notice

def noticeall(ISO):
    for data in api_data:
        if data['iso_code'] == ISO:
            allnotice = data['notice'].split('\r\n')
            return allnotice