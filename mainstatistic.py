import json
from flask.json import jsonify
import pandas as pd
import numpy as np
def board_data():

    with open('./static/Test_json/corona_data.json','r') as f:
        coronadata = json.load(f)
    with open('./json_file/country_kr_ISO.json','r') as f:
        kr_country = json.load(f)
    with open('./static/Test_json/corona_vaccine_data.json','r') as f:
        vaccinedata = json.load(f)
    
    corona_df = pd.DataFrame(coronadata)
    kr_country_df = pd.DataFrame(kr_country)
    vaccine_df = pd.DataFrame(vaccinedata)
    board_data = corona_df.merge(vaccine_df,on='iso_code',how='left')
    board_data = board_data.merge(kr_country_df,on="iso_code",how='left')

    # fully vaccinated의 null값과 -1 값 처리 ==> 평균에서는 영향을 끼치지 않는 Nan 값으로 변경
    board_data.loc[board_data['fully_vaccinated']==-1,'fully_vaccinated'] = np.NaN
    board_data.loc[board_data['total_cases']==-1,'fully_vaccinated'] = np.NaN
    chart = board_data.groupby('continent').mean()
    chart_data =[
        {'continent':"Africa",'data':[int(chart.loc['Africa',['total_cases']]),int(chart.loc['Africa','fully_vaccinated'])]},
        {'continent':'South America','data':[int(chart.loc['America',['total_cases']]),int(chart.loc['America','fully_vaccinated'])]},
        {'continent':'North America','data':[int(chart.loc['NorthernAmerica','total_cases']),int(chart.loc['NorthernAmerica','fully_vaccinated'])]},
        {'continent':'Europe','data':[int(chart.loc['Europe','total_cases']),int(chart.loc['Europe','fully_vaccinated'])]},
        {'continent':'Aisa','data':[int(chart.loc['Asia','total_cases']),int(chart.loc['Asia','fully_vaccinated'])]},
        {'continent':'Oceania','data':[int(chart.loc['Oceania','total_cases']),int(chart.loc['Oceania','fully_vaccinated'])]}
    ]

    # json 처리를 위한 NAn값 다시 변경
    for i in board_data.columns:
        board_data.loc[board_data[i].isnull(),i] = -1
    board_data = board_data.to_dict(orient='records')
    print(type(board_data))
    return {'chart_data':chart_data,"merged":board_data}