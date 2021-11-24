import pymysql
import datetime
import json


# # 기본 폼 (복붙용)
# # comment_data.append({"iso_code" : "", "parent" : , "text" : "", "nickname" : "", "like" : , "dislike" : , "write_time" : "", "password" : ""})
# comment_data = []
# comment_data.append({"iso_code" : "US", "parent" : 1, "text" : "asdf", "nickname" : "xcvb", "write_time" : "1998-12-31 23:59:59", "password" : "asdfxb"})
# comment_data.append({"iso_code" : "US", "parent" : 1, "text" : "zxcv", "nickname" : "sefb", "write_time" : "1998-12-31 23:59:59", "password" : "xcvbsdfb"})
# comment_data.append({"iso_code" : "US", "parent" : 3, "text" : "qwer", "nickname" : "asvarew", "write_time" : "1998-12-31 23:59:59", "password" : "dxvb"})
# comment_data.append({"iso_code" : "US", "parent" : 3, "text" : "cxvbsb", "nickname" : "xcnn", "write_time" : "1998-12-31 23:59:59", "password" : "sgbr"})
# comment_data.append({"iso_code" : "RU", "parent" : 5, "text" : "xcvb", "nickname" : "esbx", "write_time" : "1998-12-31 23:59:59", "password" : "fgndf"})
# comment_data.append({"iso_code" : "RU", "parent" : 5, "text" : "sdfbds", "nickname" : "mhjf", "write_time" : "1998-12-31 23:59:59", "password" : "cvbe"})
# comment_data.append({"iso_code" : "RU", "parent" : 7, "text" : "srn", "nickname" : "tmt", "write_time" : "1998-12-31 23:59:59", "password" : "sbrt"})
# comment_data.append({"iso_code" : "RU", "parent" : 7, "text" : "rymfgcnrd", "nickname" : "tncs", "write_time" : "1998-12-31 23:59:59", "password" : "fdbgdf"})
# comment_data.append({"iso_code" : "US", "parent" : 9, "text" : "asdf", "nickname" : "xcvb", "write_time" : "1998-12-31 23:59:59", "password" : "asdfxb"})
# comment_data.append({"iso_code" : "US", "parent" : 1, "text" : "zxcv", "nickname" : "sefb", "write_time" : "1998-12-31 23:59:59", "password" : "xcvbsdfb"})
# comment_data.append({"iso_code" : "US", "parent" : 3, "text" : "qwer", "nickname" : "asvarew", "write_time" : "1998-12-31 23:59:59", "password" : "dxvb"})
# comment_data.append({"iso_code" : "US", "parent" : 12, "text" : "cxvbsb", "nickname" : "xcnn", "write_time" : "1998-12-31 23:59:59", "password" : "sgbr"})
# comment_data.append({"iso_code" : "RU", "parent" : 13, "text" : "xcvb", "nickname" : "esbx", "write_time" : "1998-12-31 23:59:59", "password" : "fgndf"})
# comment_data.append({"iso_code" : "RU", "parent" : 13, "text" : "sdfbds", "nickname" : "mhjf", "write_time" : "1998-12-31 23:59:59", "password" : "cvbe"})
# comment_data.append({"iso_code" : "RU", "parent" : 15, "text" : "srn", "nickname" : "tmt", "write_time" : "1998-12-31 23:59:59", "password" : "sbrt"})
# comment_data.append({"iso_code" : "RU", "parent" : 7, "text" : "rymfgcnrd", "nickname" : "tncs", "write_time" : "1998-12-31 23:59:59", "password" : "fdbgdf"})


# conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
# cur = conn.cursor()
# cur.execute('TRUNCATE TABLE comment') # 테이블 레코드 비우기

# # 4. 해당 테이블에 데이터 추가
# for i in range(len(comment_data)):
#     cur.execute('INSERT INTO comment VALUES(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(\
#     comment_data[i]["iso_code"], \
#     int(comment_data[i]["parent"]), \
#     comment_data[i]["text"], \
#     comment_data[i]["nickname"], \
#     comment_data[i]["write_time"], \
#     comment_data[i]["password"]))

# conn.commit()
# conn.close()
# print("comment_data table update complete")

conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
cur = conn.cursor()

cur.execute("select * from comment order by parent desc;")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
comment_data=[]
for result in rv:
    comment_data.append(dict(zip(row_headers,result)))
conn.close()

file_path = "../static/Test_json/comment.json"
with open(file_path, 'w') as outfile:
    json.dump(comment_data, outfile)