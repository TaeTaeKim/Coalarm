from selenium import webdriver
import time
import re
import json

dict = []  # 국가별 코로나 정보를 저장할 딕셔너러

# 웹사이트 실행
with webdriver.Chrome() as driver:
    driver.get('https://coronaboard.kr/en/')

    # 더보기 버튼 누르기 (스크롤 후 버튼 클릭)
    for i in range(2):
        time.sleep(5)
        try:
            some_element = driver.find_element_by_id('show-more')
            some_element.click()
        except: print("시간이 부족합니다.")                            # time.sleep 적절한 값 찾기
    # table 읽기
    table = driver.find_element_by_tag_name('tbody')
    tr = table.find_elements_by_tag_name('tr')

    # 나라별 결과 나누기
    result = []
    for t in tr:
        info = t.text
        result.append(info)

    for r in result:
        data = r.split('\n')
        if len(data) == 4:
            a = data[0]     # index, country_name, total_confirmed
            b = data[1]     # new_confirmed, total_deaths
            c = data[2]     # new_deaths, total_recovered
            d = data[3]     # new_recovered, fatality, recovery, incidence
        else:
            a = data[0]     # index, country_name, total_confirmed
            b = data[1]     # new_confirmed, total_deaths
            c = "N/A"       # new_deaths, total_recovered
            d = data[2]     # new_recovered, fatality, recovery, incidence

        # 데이터 컬럼별로 나누기 (a)
        try:
            country_name = re.search('[A-Za-z]+[\s]?[A-Za-z]+', a).group()
            total_confirmed = re.search('[\d+,?]+\d{3}$', a).group()
        except:
            total_confirmed = a.split(' ')[-1]              # 정규식으로 걸러지지 않은 값


        # 데이터 컬럼별로 나누기 (b와 c)
        if b.startswith('('):
            new_confirmed, total_deaths  = b.split(" ")
        else:
            new_confirmed, total_deaths = 'N/A', b

        if c.startswith('('):
            new_deaths, total_recovered = c.split(" ")
        else:
            new_deaths, total_recovered = 'N/A', c

        # 데이터 컬럼별로 나누기 (d) ---> 경우의 수 3개
        d_list = d.split()
        if len(d_list) == 3:
            fatality, recovery, incidence = d.split(" ")
        elif len(d_list) == 4:
            new_recovered, fatality, recovery, incidence = d.split()
        else:
            new_deaths, new_recovered, fatality, recovery, incidence = d.split()

        # 데이터 형변환 및 결측값 처리

        try: total_confirmed = int(total_confirmed.replace(",", ""))  # , 제거 후 int로 변환
        except: total_confirmed = -1

        try: new_confirmed = int(new_confirmed[2:-1].replace(',', ''))  # new_confirmed값이 있는경우 (+)삭제하고 int 변환
        except: new_confirmed = -1

        try: total_deaths = int(total_deaths.replace(',', ''))  # total_deaths값 int로 변환
        except: total_deaths = -1

        try: new_deaths = int(new_deaths[2:-1].replace(',', ''))  # new_confirmed값이 있는경우 (+)삭제하고 int 변환
        except: new_deaths = -1

        try: total_recovered = int(total_recovered.replace(',', ''))  # total_recovered값 int 변환
        except: total_recovered = -1

        try : new_recovered = int(new_recovered[2:-1].replace(',', '')) # new_recovered값 int 변환
        except: new_recovered = -1

        try : fatality = float(fatality)
        except: fatality = -1

        try: recovery = float(recovery)
        except: recovery = -1

        try: incidence = int(incidence.replace(',',''))
        except: incidence = -1


        data = {
            'country_name' : country_name,
            'total_confirmed' : total_confirmed,
            'new_confirmed' : new_confirmed,
            'total_deaths' : total_deaths,
            'new_deaths' : new_deaths,
            'total_recovered' : total_recovered,
            'new_recovered' : new_recovered,
            'fatality' : fatality,
            'recovery' : recovery,
            'incidence': incidence
        }

        dict.append(data)

    with open ('./covid_info.json', 'w') as f:
        json.dump(dict, f)