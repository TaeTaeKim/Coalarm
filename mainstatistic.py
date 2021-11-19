import json
import pandas as pd
def board_data():

    with open('./static/Test_json/corona_data.json','r') as f:
        coronadata = json.load(f)

    corona_df = pd.DataFrame(coronadata)
    continent_corona = corona_df.groupby(['continent']).mean()['total_cases']

    with open('./static/Test_json/corona_vaccine_data.json','r') as f:
        vaccinedata = json.load(f)
    for i in vaccinedata:
        if i['iso_code'] =="Africa":
            africa_vaccine = i['fully_vaccinated']
        elif i['iso_code'] == 'South America':
            S_America_vaccine = i['fully_vaccinated']
        elif i['iso_code'] == 'North America':
            N_America_vaccine = i['fully_vaccinated']
        elif i['iso_code'] =='Europe':
            europe_vaccine = i['fully_vaccinated']
        elif i['iso_code'] == "Asia":
            asia_vaccine  = i['fully_vaccinated']
        elif i['iso_code'] == "Oceania":
            oceania_vaccine = i['fully_vaccinated']
    chart_data =[
        {'continent':"Africa",'data':[continent_corona['Africa'],africa_vaccine]},
        {'continent':'South America','data':[continent_corona['America'],S_America_vaccine]},
        {'continent':'North America','data':[continent_corona['NorthernAmerica'],N_America_vaccine]},
        {'continent':'Europe','data':[continent_corona['Europe'],europe_vaccine]},
        {'continent':'Aisa','data':[continent_corona['Asia'],asia_vaccine]},
        {'continent':'Oceania','data':[continent_corona['Oceania'],oceania_vaccine]}
    ]

    vaccine_df = pd.DataFrame(vaccinedata)
    merged = corona_df.merge(vaccine_df,on='iso_code',how='inner')
    merged = merged.to_dict(orient='records')
    return {'chart_data':chart_data,"merged":merged}