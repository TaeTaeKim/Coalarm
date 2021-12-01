import json
import pymysql
import pandas as pd
import numpy as np
def board_data():

    with open('./json_file/country_kr_ISO.json','r') as f:
            kr_country = json.load(f)

    # db select query 
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
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

    conn.close()

    corona_df = pd.DataFrame(coronadata)
    kr_country_df = pd.DataFrame(kr_country)
    vaccine_df = pd.DataFrame(vaccinedata)
    board_data = corona_df.merge(vaccine_df,on='iso_code',how='left')
    board_data = board_data.merge(kr_country_df,on="iso_code",how='left')

    # fully vaccinated의 null값과 -1 값 처리 ==> 평균에서는 영향을 끼치지 않는 NaN 값으로 변경
    board_data.loc[board_data['fully_vaccinated']==-1,'fully_vaccinated'] = np.NaN
    board_data.loc[board_data['total_cases']==-1,'fully_vaccinated'] = np.NaN
    chart = board_data.groupby('continent').mean()
    chart_data =[
        {'continent':"Africa",'data':[int(chart.loc['Africa',['total_caeses_per_1million_population']]),int(chart.loc['Africa','fully_vaccinated'])]},
        {'continent':'South America','data':[int(chart.loc['America',['total_caeses_per_1million_population']]),int(chart.loc['America','fully_vaccinated'])]},
        {'continent':'North America','data':[int(chart.loc['NorthernAmerica','total_caeses_per_1million_population']),int(chart.loc['NorthernAmerica','fully_vaccinated'])]},
        {'continent':'Europe','data':[int(chart.loc['Europe','total_caeses_per_1million_population']),int(chart.loc['Europe','fully_vaccinated'])]},
        {'continent':'Aisa','data':[int(chart.loc['Asia','total_caeses_per_1million_population']),int(chart.loc['Asia','fully_vaccinated'])]},
        {'continent':'Oceania','data':[int(chart.loc['Oceania','total_caeses_per_1million_population']),int(chart.loc['Oceania','fully_vaccinated'])]}
    ]

    # json 처리를 위한 NaN값 다시 변경
    for i in board_data.columns:
        board_data.loc[board_data[i].isnull(),i] = -1
    board_data = board_data.to_dict(orient='records')
    return {'chart_data':chart_data,"merged":board_data}
