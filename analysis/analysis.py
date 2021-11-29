#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:22:05 2021

@author: bizzy


안전 지수
1. 백신 접종율 높고           'fully_vaccinated'   nan -> 0
2. 현재 인구대비 확진자 적고    'total_caeses_per_1million_population'
3. 완치율 높고               'recovered'
4. 치명율 낮고               'critical'
5. 살인 사건 발생율 낮고       'homicide_rate'
6. 여행 경보 수치 낮고         'alarm_lvl' nan -> 2

0 백신 안맞음
1 발생율
2 완치율
3 치명율
4 살인율
5 여행경
"""
from geochart_iso_from_csv import geochart_iso_from_csv
from get_safety_data import get_safety_data


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
import json

# 안전점수 테이블 만들기

# ISO codes in Geochart
iso = geochart_iso_from_csv()

# corona vaccine data, 접종율
with open('./json/corona_vaccine_data.json', 'r') as f:
    vaccinated = json.load(f)


# corona data, 발생율,완치율,치명율
with open('./json/corona_data.json', 'r') as f:
    confirmed = json.load(f)

for c in confirmed:
    c['critical'] = c.pop('recovered_ratio')
    c['recovered'] = c.pop('critical_ratio')



# homicide data, 살인률 DB에서 꺼내면 None , GEOCHART에 없는애들은 -1
with open('./json/safety_data.json', 'r') as f:
    safety = json.load(f)

# alarm_lvl, 여행경보
url = 'http://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2'
params ={'serviceKey' : 'l2Tz12aLRivDhn4CKg0XE5RGdY4wc7asf9UaKQmF6ZRiigW0klMF5ioFkBI47WiY0XTahwpsqMYX1l9Kl6gaWg==',
        'returnType' : 'JSON',
        'numOfRows' : '200',
        'pageNo' : '1' }

response = requests.get(url, params=params)
result =response.json()
data_level = result['data']


new = []
for i in iso:
    n = {}
    for c in confirmed:
        if i == c['iso_code']:   
            n['iso_code'] = i
            n['total_caeses_per_1million_population'] = c['total_caeses_per_1million_population']
            n['recovered'] = c['recovered']
            n['critical'] = c['critical']
    for v in vaccinated:
        if i == v['iso_code']:  
            n['fully_vaccinated'] = v['fully_vaccinated']
    for s in safety:
        if i == s['iso_code']:  
            n['homicide_rate'] = float(s['homicide_rate'])
    for d in data_level:
        if i == d['country_iso_alp2']:
            n['lvl'] = d['alarm_lvl']
    new.append(n)

# iso 코드 없는데 값이 있는 데이터 제검
new2 = []
for n in new:
    if len(n) > 2:
        new2.append(n)

'''
형식
{ 대륙이름 : [iso_code1, iso_code2, ...] }
'''
continent = {
'NorthernAfrica': [
    'DZ', 'EG', 'EH', 'LY', 'MA', 'SD', 'SS', 'TN'
],
'WesternAfrica': [
    'BF', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'LR', 'ML',
    'MR', 'NE', 'NG', 'SH', 'SL', 'SN', 'TG'
],
'MiddleAfrica': [
    'AO', 'CD', 'ZR', 'CF', 'CG', 'CM', 'GA', 'GQ', 'ST', 'TD'
],
'EasternAfrica': [
    'BI', 'DJ', 'ER', 'ET', 'KE', 'KM', 'MG', 'MU', 'MW', 'MZ', 
    'RE', 'RW', 'SC', 'SO', 'TZ', 'UG', 'YT', 'ZM', 'ZW'
],
'SouthernAfrica': [
    'BW', 'LS', 'NA', 'SZ', 'ZA'
],
'NorthernEurope': [
    'GG', 'JE', 'AX', 'DK', 'EE', 'FI', 'FO', 'GB', 'IE', 'IM', 
    'IS', 'LT', 'LV', 'NO', 'SE', 'SJ'
],
'WesternEurope': [
    'AT', 'BE', 'CH', 'DE', 'DD', 'FR', 'FX', 'LI', 'LU', 'MC', 'NL'
],
'EasternEurope': [
	'BG', 'BY', 'CZ', 'HU', 'MD', 'PL', 'RO', 'RU', 'SU', 'SK', 'UA'
],
'SouthernEurope': [
	'AD', 'AL', 'BA', 'ES', 'GI', 'GR', 'HR', 'IT', 'ME', 'MK',
    'MT', 'RS', 'PT', 'SI', 'SM', 'VA', 'YU'
],
'NorthernAmerica': [
	'BM', 'CA', 'GL', 'PM', 'US'
],
'Caribbean': [
    'AG', 'AI', 'AN', 'AW', 'BB', 'BL', 'BS', 'CU', 'DM', 'DO', 
    'GD', 'GP', 'HT', 'JM', 'KN', 'KY', 'LC', 'MF', 'MQ', 'MS', 
    'PR', 'TC', 'TT', 'VC', 'VG', 'VI'
],
'CentralAmerica': [
    'BZ', 'CR', 'GT', 'HN', 'MX', 'NI', 'PA', 'SV'
],
'SouthAmerica': [
	'AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'FK', 'GF', 'GY', 'PE', 
    'PY', 'SR', 'UY', 'VE'
],
'CentralAsia': [
    'TM', 'TJ', 'KG', 'KZ', 'UZ'
],
'EasternAsia': [
    'CN', 'HK', 'JP', 'KP', 'KR', 'MN', 'MO', 'TW'
],
'SouthernAsia': [
    'AF', 'BD', 'BT', 'IN', 'IR', 'LK', 'MV', 'NP', 'PK'
],
'SouthEasternAsia': [
    'BN', 'ID', 'KH', 'LA', 'MM', 'BU', 'MY', 'PH', 'SG', 'TH', 
    'TL', 'TP', 'VN'
],
'WesternAsia': [	
    'AE', 'AM', 'AZ', 'BH', 'CY', 'GE', 'IL', 'IQ', 'JO', 'KW', 
    'LB', 'OM', 'PS', 'QA', 'SA', 'NT', 'SY', 'TR', 'YE', 'YD'
],
'Oceania': [
    'AU', 'NF', 'NZ'
],
'Melanesia': [
	'FJ', 'NC', 'PG', 'SB', 'VU'
],
'Micronesia': [
    'FM', 'GU', 'KI', 'MH', 'MP', 'NR', 'PW'
],
'Polynesia': [
	'AS', 'CK', 'NU', 'PF', 'PN', 'TK', 'TO', 'TV', 'WF', 'WS'
]
}
# 대륙이름 column 추가
for n in new2:
    for c in continent.items():
        if n['iso_code'] in c[1]:
            n['continent'] = c[0]

# 나라이름 column 추가
with open('./json/country_ISO.json', 'r') as f:
    kr = json.load(f)
         
for n in new2:
    for c in kr:
        if n['iso_code'] == c['Code']:
            n['Name'] = c['Name']


a = pd.DataFrame(new2)
# -1 -> nan
a.loc[a['total_caeses_per_1million_population']==-1,'total_caeses_per_1million_population'] = np.NaN
a.loc[a['recovered']==-1,'recovered'] = np.NaN
a.loc[a['critical']==-1, 'critical'] = np.NaN
a.loc[a['fully_vaccinated']==-1,'fully_vaccinated'] = np.NaN
a.loc[a['homicide_rate']==-1,'homicide_rate'] = np.NaN

# 대륙별 평균
total_continent = a['total_caeses_per_1million_population'].groupby(a['continent']).mean()
recovered_continent = a['recovered'].groupby(a['continent']).mean()
critical_continent = a['critical'].groupby(a['continent']).mean()
vaccinated_continent = a['fully_vaccinated'].groupby(a['continent']).mean()
homicide_continent = a['homicide_rate'].groupby(a['continent']).mean()


# # 치명률 -1 -> nan
# for i in range(len(a)):
#     if a['critical'][i] == -1:
#         a['critical'][i] = np.nan
# critical_continent = a['critical'].groupby(a['continent']).mean()


# nan 채우기 대륙 평균
for i in range(len(a)):
    # 발생율 nan -> 대륙 발생율 평균
    if np.isnan(a['total_caeses_per_1million_population'][i]):
        a['total_caeses_per_1million_population'][i] = total_continent[a['continent'][i]]
    # 회복율 nan -> 대륙 회복율 평균
    if np.isnan(a['recovered'][i]):
        a['recovered'][i] = recovered_continent[a['continent'][i]]
    # 치명율 -> 대륙 치명율 평균
    if np.isnan(a['critical'][i]):
        a['critical'][i] = critical_continent[a['continent'][i]]
    # 백신접종률 -> 대륙 백신접종률 평균
    if np.isnan(a['fully_vaccinated'][i]):
        a['fully_vaccinated'][i] = vaccinated_continent[a['continent'][i]]
    # 살인률 nan -> 대륙 살인률 평균
    if np.isnan(a['homicide_rate'][i]):
        a['homicide_rate'][i] = homicide_continent[a['continent'][i]]
    # 여행경보 nan -> 2
    if np.isnan(a['lvl'][i]):
        a['lvl'][i] = 2

# nan 채우기 전체 평균        
critical_last = a['critical'].mean()
vaccinated_last = a['fully_vaccinated'].mean()
homicide_last = a['homicide_rate'].mean()
for i in range(len(a)):
    # 치명율 -> 전체 치명율 평균
    if np.isnan(a['critical'][i]):
        a['critical'][i] = critical_last
    # 백신접종률 -> 전체 백신접종률 평균
    if np.isnan(a['fully_vaccinated'][i]):
        a['fully_vaccinated'][i] = vaccinated_last
    # 살인률 nan -> 전체 살인률 평균
    if np.isnan(a['homicide_rate'][i]):
        a['homicide_rate'][i] = homicide_last


def decrease_variable(x):
    return max(x) - x

def normalize(x):
    return (x - min(x)) / (max(x) - min(x))

X = np.empty((217, 6))
X[:, 0] = a['total_caeses_per_1million_population']
X[:, 0] = decrease_variable(X[:, 0])
X[:, 0] = normalize(X[:, 0])
#높
X[:, 1] = a['recovered']
X[:, 1] = normalize(X[:, 1])

X[:, 2] = a['critical']
X[:, 2] = decrease_variable(X[:, 2])
X[:, 2] = normalize(X[:, 2])
#높
X[:, 3] = a['fully_vaccinated']
X[:, 3] = normalize(X[:, 3])

X[:, 4] = a['homicide_rate']
X[:, 4] = decrease_variable(X[:, 4])
X[:, 4] = normalize(X[:, 4])

X[:, 5] = a['lvl']
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
'''
# a['score3'] = [0]*217
# for i in range(217):
#     y1 = np.dot(v[:,0], X[i])
#     y2 = np.dot(v[:,1], X[i])
#     y3 = np.dot(v[:,2], X[i])
    
#     y = np.array([y1,y2,y3]).reshape(1,3)
#     ratio = (w[:3]/w.sum()).reshape(3,1)
#     print(y, ratio)
#     a.loc[i,'score3'] = np.dot(y,ratio)[0][0]
a['score4'] = [0]*217
for i in range(217):
    y1 = np.dot(v[:,0], X[i])
    y2 = np.dot(v[:,1], X[i])
    y3 = np.dot(v[:,2], X[i])
    y4 = np.dot(v[:,3], X[i])
    y5 = np.dot(v[:,4], X[i])
    y6 = np.dot(v[:,5], X[i])
    
    y = np.array([y1,y2,y3,y4,y5,y6]).reshape(1,6)
    ratio = (w/w.sum()).reshape(6,1)
    print(y, ratio)
    a.loc[i,'score4'] = np.dot(y,ratio)[0][0]

x_std1 = np.std(X[:, 0], ddof = 1)    
x_std2 = np.std(X[:, 1], ddof = 1)    
x_std3 = np.std(X[:, 2], ddof = 1)    
x_std4 = np.std(X[:, 3], ddof = 1)    
x_std5 = np.std(X[:, 4], ddof = 1)    
x_std6 = np.std(X[:, 5], ddof = 1)    

x_std = np.array([x_std1,x_std2,x_std3,x_std4,x_std5,x_std6])
std = np.dot(x_std.reshape(6,1), x_std.reshape(1,6))
coff = X_cov / std
    
X2 = np.empty((217, 6))
X2[:, 0] = a['total_caeses_per_1million_population']
# X2[:, 0] = decrease_variable(X2[:, 0])
X2[:, 0] = normalize(X2[:, 0])
#높
X2[:, 1] = a['recovered']
X2[:, 1] = normalize(X2[:, 1])

X2[:, 2] = a['critical']
# X2[:, 2] = decrease_variable(X2[:, 2])
X2[:, 2] = normalize(X2[:, 2])
#높
X2[:, 3] = a['fully_vaccinated']
X2[:, 3] = normalize(X2[:, 3])

X2[:, 4] = a['homicide_rate']
# X2[:, 4] = decrease_variable(X2[:, 4])
X2[:, 4] = normalize(X2[:, 4])

X2[:, 5] = a['lvl']
# X2[:, 5] = decrease_variable(X2[:, 5])
X2[:, 5] = normalize(X2[:, 5])


X2_cen = X2 - X2.mean(axis=0)  # 평균을 0으로
X2_cov = np.dot(X2_cen.T, X2_cen) / 59

w, v = np.linalg.eig(X2_cov)
rate = w/w.sum()
print('explained variance ratio :', w / w.sum())

a['score2'] = (rate[0] * X2[:, 1]+\
    rate[1] * X2[:, 1] +\
    rate[2] * X2[:, 2] +\
    rate[3] * X2[:, 3] +\
    rate[4] * X2[:, 4] +\
    rate[5] * X2[:, 5]
)*100
'''   
          
          