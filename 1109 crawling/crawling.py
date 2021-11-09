import requests
import json
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
# tags = soup.select("table tbody tr td em")    # soup.select("#_per")

tags = soup.find("table", id="main_table_countries_today")
tbody = tags.tbody.prettify()

a = tags.tbody.select('tr')
result = []
for i in a:
    result.append(i.text.split('\n'))

datas = []
for r in result[8:]:
    country_info = {
            'country_name' : r[2],
            'active_case': r[9].replace(",", ""),
            # 'new_cases' : r[4],
            'total_death': r[5][:-1].replace(",", ""),
            # ' new_death' : r[6],
    }
    
    datas.append(country_info)
data = sorted(datas, key = lambda x : x["country_name"])
print(datas)