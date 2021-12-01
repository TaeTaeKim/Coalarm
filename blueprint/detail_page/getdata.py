
import pymysql

# db select query
conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
cur = conn.cursor()
cur.execute("select * from Corona_Data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
coronadata=[]
for result in rv:
    coronadata.append(dict(zip(row_headers,result)))

conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
cur = conn.cursor()
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

cur.execute("select * from Embassy_Data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
embassy_data=[]
for result in rv:
    embassy_data.append(dict(zip(row_headers,result)))

cur.execute("select * from Safety_Score")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
safe_data=[]
for result in rv:
    safe_data.append(dict(zip(row_headers,result)))

conn.close()

inbound = ["목적", "외국인", "한국", "해외입국자","금지", "허용", "중단","허가","허용","불허","제한","통제","폐쇄","불가","관광","중지","통제"]
document = ["확인서", "허가증", "신고서", "서약서","온라인","결과서","PCR","검사","카드","보험","증명서","QR","디지털","필수","결과지","서류","검진서","검사서","공인서"]
def corona(ISO):
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
            if data['notice'] =='None':
                return "no data"
            else:
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
        if data['iso_code'] == ISO:
            if data['notice'] =='None':
                return "no data"
            else:
                allnotice = data['notice'].split('\r\n')
                return allnotice
#
def embassy(ISO):
    embassydata = []
    for data in embassy_data:
        if data['iso_code'] == ISO:
            embassydata.append(data)
    return embassydata

def safe(ISO):
    for data in safe_data:
        if data['iso_code'] ==ISO:
            return data
