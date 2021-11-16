import json
with open('./json_file/api_data.json', 'r') as f:
    b = json.load(f)

print(b)