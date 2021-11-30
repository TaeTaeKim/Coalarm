import pymysql
import datetime
import json
import pandas as pd
import numpy as np


# # 기본 폼 (복붙용)
# comment_data.append({"iso_code" : "", "parent" : , "text" : "", "nickname" : "", "like" : , "dislike" : , "write_time" : "", "password" : ""})
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

# # db 입력 폼
# conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
# cur = conn.cursor()
# cur.execute('TRUNCATE TABLE Comment') # 테이블 레코드 비우기

# # 4. 해당 테이블에 데이터 추가
# for i in range(len(comment_data)):
#     cur.execute('INSERT INTO Comment VALUES(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(\
#     comment_data[i]["iso_code"], \
#     int(comment_data[i]["parent"]), \
#     comment_data[i]["text"], \
#     comment_data[i]["nickname"], \
#     comment_data[i]["write_time"], \
#     comment_data[i]["password"]))

# conn.commit()
# conn.close()
# print("comment_data table update complete")

# 코멘트 차례대로 읽기
# conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
# cur = conn.cursor()
# cur.execute("select * from Comment order by parent desc;")
# row_headers=[x[0] for x in cur.description]
# rv = cur.fetchall()
# comment_data=[]
# for result in rv:
#     comment_data.append(dict(zip(row_headers,result)))
# conn.close()

# file_path = "../static/Test_json/comment.json"
# with open(file_path, 'w') as outfile:
#     json.dump(comment_data, outfile)

# 안전점수 데이터 서빙
# with open('./json_file/new_continent.json', 'r') as f:
#     df_continent = pd.DataFrame(json.load(f))  # json_country key : ["iso_code", "continent"]

# conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
# cur = conn.cursor()

# cur.execute("select v.iso_code, v.fully_vaccinated, s.homicide_rate, a.caution, c.total_caeses_per_1million_population, c.recovered_ratio, c.critical_ratio \
# from Corona_Vaccine_Data v \
# join Safety_Data s using(iso_code) \
# join Api_Data a using(iso_code) \
# join Corona_Data c using(iso_code)")
# row_headers=[x[0] for x in cur.description]
# rv = cur.fetchall()
# recommend_data=[]
# for result in rv:
#     recommend_data.append(dict(zip(row_headers,result)))
# conn.close()

# df_recommend_data = pd.DataFrame(recommend_data).replace(-1, np.NaN)
# df_recommend_data["caution"] = df_recommend_data["caution"].apply(lambda x : x if x != 5 else 1.5)
# df_recommend_data = pd.merge(df_continent, df_recommend_data, how = 'left', on = "iso_code").groupby("continent").apply(lambda x: x.fillna(x.mean()))
# df_recommend_data = df_recommend_data.drop(["continent"], axis=1).reset_index()
# df_recommend_data = df_recommend_data.fillna(df_recommend_data.mean())
# # df_recommend_data = df_recommend_data.dropna(axis=0)
# df_recommend_data = df_recommend_data.to_dict(orient = "records")
# for i in df_recommend_data:
#     print(i)

# file_path = "./recommend.json
# with open(file_path, 'w') as outfile:
#     json.dump(df_recommend_data, outfile)


# select v.iso_code, v.fully_vaccinated, s.homicide_rate, a.caution, c.total_caeses_per_1million_population, c.recovered_ratio, c.critical_ratio
# from corona_vaccine_data v
# join safety_data s using(iso_code)
# join api_data a using(iso_code)
# join corona_data c using(iso_code);
# limit 10;

# db 읽기 폼
# conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
# cur = conn.cursor()
# cur.execute("select * from Exchange_Data")
# row_headers=[x[0] for x in cur.description]
# rv = cur.fetchall()
# response_text_dict=[]
# for result in rv:
#     response_text_dict.append(dict(zip(row_headers,result)))
# conn.close()