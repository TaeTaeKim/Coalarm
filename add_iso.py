import json


with open('./coalarm_1.0/json_file/country_ISO.json', 'r') as f:
    iso_code = json.load(f)

iso_code.append({'Code': 'MO', 'Name': 'Macau'})
iso_code.append({'Code': 'MK', 'Name': 'Macedonia'})
iso_code.append({'Code': 'VC', 'Name': 'St Vincent and The Grenadines'})
iso_code.append({'Code': 'DO', 'Name': 'Dominican republic'})
iso_code.append({'Code': 'CD', 'Name': 'Republic of the Congo'})
iso_code.append({'Code': 'GW', 'Name': 'Guinea Bissau'})
iso_code.append({'Code': 'KP', 'Name': 'North Korea'})

with open('./coalarm_1.0/json_file/country_ISO.json', 'w') as f:
    json.dump(iso_code, f)


# iso_dict = {}
# for index in iso_code:
#     iso_dict[index["Name"]] = index["Code"]
    
    

# with open('./coalarm_1.0/json_file/country_ISO.json', 'r') as f:
#     safe_data = json.load(f)

# for idx in safe_data:
#     try:
#         idx["iso_code"] = iso_dict[idx["Country"]]
#     except:
#         failed.append(idx["Country"])



# with open('./terror.json', 'r') as f:
#     terror_data = json.load(f)

# for idx in terror_data:
#     try:
#         idx['iso_code'] = iso_dict[idx['Country']]
#     except:
#         failed2.append(idx['Country'])
        


# a = safe_data
# b = terror_data

# with open('./Safety_data.json', 'w') as f:
#     json.dump(safe_data, f)

# with open('./Terror_data.json', 'w') as f:
#     json.dump(terror_data, f)

     

