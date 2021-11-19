import json, pymysql

conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
cur = conn.cursor()
cur.execute("select * from api_data")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
response_text_dict=[]
for result in rv:
    response_text_dict.append(dict(zip(row_headers,result)))
conn.close()

with open('./new_api_data.json', 'w') as f:
    json.dump(response_text_dict, f)
