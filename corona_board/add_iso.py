import json

with open("./coalarm_1.0/json_file/country_ISO.json", "r") as f:
    add_country = json.load(f)

    add_country.append({'Code': 'KR', 'Name': 'South Korea'})
    add_country.append({'Code': 'XK', 'Name': 'Kosovo'})
    add_country.append({'Code': 'RE', 'Name': 'R\u00e9union'})    # <----- R
    add_country.append({'Code': 'TL', 'Name': 'East Timor'})
    add_country.append({'Code': 'CW', 'Name': 'Cura\u00e7ao'})   # <----Curaçao

    add_country.append({'Code': 'CG', 'Name': 'Democratic Republic of Congo'})
    add_country.append({'Code': 'BQ', 'Name': 'Bonaire Sint Eustatius and Saba'})
    add_country.append({'Code': 'CI', 'Name': "Cote d'Ivoire"})
    add_country.append({'Code': 'CW', 'Name': 'Curacao'})
    add_country.append({'Code': 'TL', 'Name': 'Timor'})


with open('./coalarm_1.0/json_file/add_country_ISO.json', 'w') as f:
    json.dump(add_country, f)
