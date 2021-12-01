
# Latest update
# 11/16 새로운 코드로 업데이트 

from selenium import webdriver
from selenium.webdriver import ActionChains
import time

def get_corona_scraping():

    dict_list = []  # 국가별 코로나 정보를 저장할 리스트

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    # driver 실행
    driver = webdriver.Chrome("./chromedriver", options=options)
    # driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get('https://coronaboard.kr/en/')
    time.sleep(1)

    for i in range(2):
        #some_element까지 스크롤
        some_element = driver.find_element_by_xpath('//*[@id="global-slide"]/div/div[3]/p/a')
        action = ActionChains(driver)
        action.move_to_element(some_element).perform()
        time.sleep(1)

        #더보기 클릭
        more_data = driver.find_element_by_xpath('//*[@id="show-more"]')
        more_data.click()
        time.sleep(1)

    # table 읽기
    table = driver.find_element_by_tag_name('tbody')
    tr = table.find_elements_by_tag_name('tr')
    for t in tr:
        td_ele = t.find_elements_by_tag_name('td')
        country_name = td_ele[1].text[:-2]
        confirmed = td_ele[2].text.replace('\n','')
        deaths = td_ele[3].text.replace('\n','')
        recovered = td_ele[4].text.replace('\n','')
        recovery = td_ele[6].text
        fatality = td_ele[5].text
        incidence = td_ele[7].text

        if "Japan" in country_name:   # Japan은 * 하나 붙어있음.
            country_name = country_name[:-1]

        if '(' in confirmed:
            total_confirmed, new_confirmed = confirmed.split('(')
        else:
            total_confirmed, new_confirmed = confirmed, 'N/A'

        if '(' in deaths:
            total_deaths, new_deaths = deaths.split("(")
        else:
            total_deaths, new_deaths = deaths, 'N/A'

        if '(' in recovered:
            total_recovered, new_recovered = recovered.split("(")
        else:
            total_recovered, new_recovered = recovered,'N/A'

        # 데이터 형변환 및 결측값 처리
        try:
            total_confirmed = int(total_confirmed.replace(',', ''))
        except:
                total_confirmed = -1

        try:
            new_confirmed = int(new_confirmed[1:-1].replace(',', ''))
        except:
            new_confirmed = -1

        try:
            total_deaths = int(total_deaths.replace(',', ''))
        except:
            total_deaths = -1

        try:
            new_deaths = int(new_deaths[1:-1].replace(',', ''))
        except:
            new_deaths = -1

        try:
            total_recovered = int(total_recovered.replace(',', ''))
        except:
            total_recovered = -1

        try:
            new_recovered = int(new_recovered[1:-1].replace(',', ''))
        except:
            new_recovered = -1

        try:
            recovery = float(recovery)
        except:
            recovery = -1.0

        try:
            fatality = float(fatality)
        except:
            fatality = -1.0

        try:
            incidence = int(incidence.replace(',', ''))
        except:
            incidence = -1

        data = {
                'country_name': country_name,
                'total_confirmed': total_confirmed,
                'new_confirmed': new_confirmed,
                'total_deaths': total_deaths,
                'new_deaths': new_deaths,
                'total_recovered': total_recovered,
                'new_recovered': new_recovered,
                'recovery': recovery,
                'fatality': fatality,
                'incidence': incidence
            }
        dict_list.append(data)
    return dict_list
