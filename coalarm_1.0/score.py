#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:45:31 2021

@author: krc
"""
import numpy as np
import pandas as pd
import pymysql
import json
# conn = pymysql.connect(host='13.209.17.131', user="coalarm", password="coalarm", db="coalarm", charset="utf8")
# cur = conn.cursor()
# # cur.execute('TRUNCATE TABLE corona_data') # 테이블 레코드 비우기
# ' ec2-13-209-17-131.ap-northeast-2.compute.amazonaws.com'

# cur.execute("select * from Exchange_Data")
# row_headers=[x[0] for x in cur.description]
# rv = cur.fetchall()
# response_text_dict=[]
# for result in rv:
#     response_text_dict.append(dict(zip(row_headers,result)))
'''
새 테이블 

Safety_Score
    iso_code
    score
'''
def decrease_variable(x):
    return max(x) - x

def normalize(x):
    return (x - min(x)) / (max(x) - min(x))


def SafetyScore(new2):
    a = pd.DataFrame(new2)

    X = np.empty((len(a), 6))
    X[:, 0] = a['total_caeses_per_1million_population']
    X[:, 0] = decrease_variable(X[:, 0])
    X[:, 0] = normalize(X[:, 0])
    #높
    X[:, 1] = a['recovered_ratio']
    X[:, 1] = normalize(X[:, 1])
    
    X[:, 2] = a['critical_ratio']
    X[:, 2] = decrease_variable(X[:, 2])
    X[:, 2] = normalize(X[:, 2])
    #높
    X[:, 3] = a['fully_vaccinated']
    X[:, 3] = normalize(X[:, 3])
    
    X[:, 4] = a['homicide_rate']
    X[:, 4] = decrease_variable(X[:, 4])
    X[:, 4] = normalize(X[:, 4])
    
    X[:, 5] = a['caution']
    X[:, 5] = decrease_variable(X[:, 5])
    X[:, 5] = normalize(X[:, 5])
    
    
    X_cen = X - X.mean(axis=0)  # 평균을 0으로
    X_cov = np.dot(X_cen.T, X_cen) / 59
    
    w, v = np.linalg.eig(X_cov)
    rate = w/w.sum()
    print('explained variance ratio :', w / w.sum())
    
    a['score'] = (rate[0] * X[:, 1]+\
        rate[1] * X[:, 1] +\
        rate[2] * X[:, 2] +\
        rate[3] * X[:, 3] +\
        rate[4] * X[:, 4] +\
        rate[5] * X[:, 5]
    )*100
    return a


with open('./json_file/new_continent.json', 'r') as f:
    df_continent = pd.DataFrame(json.load(f))  # json_country key : ["iso_code", "continent"]

conn = pymysql.connect(host='localhost', user="coalarm", password="coalarm", db="coalarm", charset="utf8")
cur = conn.cursor()

cur.execute("select v.iso_code, v.fully_vaccinated, s.homicide_rate, a.caution, c.total_caeses_per_1million_population, c.recovered_ratio, c.critical_ratio \
from Corona_Vaccine_Data v \
join Safety_Data s using(iso_code) \
join Api_Data a using(iso_code) \
join Corona_Data c using(iso_code)")
row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
recommend_data=[]
for result in rv:
    recommend_data.append(dict(zip(row_headers,result)))


df_recommend_data = pd.DataFrame(recommend_data).replace(-1, np.NaN)
df_recommend_data["caution"] = df_recommend_data["caution"].apply(lambda x : x if x != 5 else 1.5)


df_recommend_data = pd.merge(df_continent, df_recommend_data, how = 'left', on = "iso_code").groupby("continent").apply(lambda x: x.fillna(x.mean()))
df_recommend_data = df_recommend_data.drop(["continent"], axis=1).reset_index()
df_recommend_data = df_recommend_data.dropna(axis=0)
df_recommend_data = df_recommend_data.to_dict(orient = "records")
print(len(df_recommend_data), type(df_recommend_data))



a = SafetyScore(df_recommend_data)
score = []
for i in range(len(a)):
    s = {}
    s['iso_code'] = a['iso_code'][i]
    s['score'] = a['score'][i]
    score.append(s)
'''
Safety_Score
    iso_code
    score
'''
for i in range(len(score)):
    cur.execute("INSERT INTO Safety_Score VALUES('{0}', '{1}', '{2}')".format(\
        score[i]["iso_code"], \
        score[i]["country_kr"], \
        float(score[i]["score"])))
conn.commit()
conn.close()
