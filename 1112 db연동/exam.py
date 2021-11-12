from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver import ActionChains

#아이디
id = "infamousgames@hanmail.net"
#비밀번호
pw = "aa1313aa"  

driver = webdriver.Chrome(r'.\chromedriver.exe')
driver.set_window_position(0, 0)
driver.set_window_size(3000, 3000)
driver.implicitly_wait(3)

#메인페이지 접속
driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
time.sleep(2)

#메인페이지 login 접속
posting = driver.find_element_by_xpath('//*[@id="standalone-header"]/div[1]/header/section[1]/div[4]/a[2]/button')
posting.click()
time.sleep(1)

#페이스북 로그인 접속
posting2 = driver.find_element_by_xpath('//*[@id="js-facebook-oauth-login"]')
posting2.click()
time.sleep(3)

#2번째(로그인 팝업창)윈도우 호출
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)

#페이스북 로그인
assert "Facebook" in driver.title 
login_box = driver.find_element_by_id("email") 
login_box.send_keys(id) 
login_box = driver.find_element_by_id("pass") 
login_box.send_keys(pw)
login_box.send_keys(Keys.RETURN)
time.sleep(6)

#1번째(메인페이지)윈도우 호출
driver.switch_to.window(driver.window_handles[0])
time.sleep(1)

driver.get('https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html')
time.sleep(10)

#id가 something인 element를 찾음
some_tag = driver.find_element_by_xpath('//*[@id="covid-signup-module"]/section/div/div[2]/div/button')

#somthing element까지 스크롤
action = ActionChains(driver)
action.move_to_element(some_tag).perform()
time.sleep(5)

#show_all 클릭
posting = driver.find_element_by_xpath('//*[@id="covid-vaccinations-tracker"]/div/div[3]/div[3]/div[1]/div/div[2]')
posting.click()
time.sleep(3)

html = driver.page_source

#크롤링
import requests
import json
from bs4 import BeautifulSoup

url = "https://www.nytimes.com/interactive/2021/world/covid-vaccinations-tracker.html"

soup = BeautifulSoup(html, "html.parser")
result = []
for i in range(1, 188):
    print(i)
    # 국가별 데이터 가져오기
    tag = soup.find(class_ = "g-row-{} svelte-oedzx3".format(i))
    # tag 에서 td 태그들을 선택하기
    td = tag.select('td')
    '''
    td[0].text: country
    td[1].text: vaccinated
    td[2].text: fully_vaccinated
    td[3].text: additional_dose
    '''
    result.append({
        'country': td[0].text,
        'vaccinated': td[1].text.split()[0],
        'fully_vaccinated': td[2].text.split()[0],
        'additional_dose': td[3].text.split()[0]
        })

print(result)