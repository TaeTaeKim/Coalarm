# Coalarm
* 해외여행에 필요한 코로나 바이러스 관련 정보를 제공한다.



## 1. 프로젝트 소개

**어떠한 데이터셋와 도구 및 기술을 사용했는지에 대한 설명과 유저에게 보이는 웹서비스에 대한 소개**


* 프로젝트와 참고 모델 : [coronaboard](https://coronaboard.kr/)

* 데이터 정보

   - 국가별 코로나 상황 데이터 :https://coronaboard.kr/en/

   - 국가별 백신 접종 데이터 : https://ourworldindata.org/covid-vaccinations

   - ISO 데이터 : https://datahub.io/core/country-list
   
   - 국기 데이터 : https://flagpedia.net/download/api

   - 여행 경보 : https://www.data.go.kr/data/15076237/openapi.do

   - 국가별 입국조치 데이터 : https://www.data.go.kr/data/15085787/openapi.do

   - 범죄 데이터 : https://globalresidenceindex.com/hnwi-index/safety-index

   - 테러 데이터 : https://tradingeconomics.com/country-list/terrorism-index

   - 환율 데이터 : https://www.koreaexim.go.kr/site/program/financial/exchange

   - 외교부 정보 데이터 :https://www.mofa.go.kr/www/pgm/m_4179/uss/emblgbd/emblgbdAdres.do / https://www.data.go.kr/data/15075354/openapi.do              

* 사용한 언어: <img src="https://media.vlpt.us/images/ajt1097/post/f37df69b-dd74-4f5b-8d45-46c8c1c0dee3/HTML&CSS.png" width="35px" height="35px" title="html_css"/> HTML/CSS,
<img src="https://t1.daumcdn.net/cfile/tistory/2149683A58CA6BF313" width="25px" height="25px" title="javascript"/> Javascript,
<img src="https://blog.fakecoding.com/content/images/wordpress/2020/06/logo-python.png" width="25px" height="25px" title="Python"/>Python,
<img src="https://ww.namu.la/s/d59b18ca16c075c57c5ebe902e14d46c58e2df1d638605017382993a696c0c8c2313077356a2bd90892fa9e00c704b6832c07c8981482d4d3b88ccb2848da731212f8457b4f40357fff71ccdbbff25ff22f7f68b2f689f12cff8839c67ca0bfa" width="35px" height="30px" title="Mysql"/> Mysql,
<img src="https://ww.namu.la/s/0627b3298410e444032557550f974b3fe63e2a533abbec95bf0eb356178fd6afa455eb65df81337b6f7889333f955dc59abac8faf6ed5cb54487f6119dac4f822d1a4933e7a81e7076130839cfe63393" width="30px" height="30px" title="AWS"/> AWS 

* 사용된 라이브러리 : requests, json, selenium, time, re, datatime, bs4, pymysql, schedule, pandas, flask, jQuery, geochart 

## 2. 프로젝트 목표

  - 국내 방역 체계가 단계적 일상 회복 '위드 코로나'로 전환되면서 어려웠던 해외여행에 대한 관심이 높아졌다. 
  하지만 나라마다 다른 방역 정책을 시행하고 있고, 필요한 정보를 제공하는 곳도 다양하기 때문에 여행하고자 하는 나라의 정보를 여러 곳에서 수집하여야 하는 불편함이 있다. 
   이를 해결하기 위해서 나라별 코로나 현황과 여행 관련 정보를 쉽게 파악할 수 있고, 안전하게 여행할 수 있는 국가를 추천하는 서비스를 개발하고자 한다. 
# 요구사항 정의서

** 프로젝트 요구사항 정리 **
1. (메인페이지) 상단
- 메인 상단 버튼을 클릭하면, 나라 검색 및 지도 영역으로 이동 

2. (메인페이지) 검색 및 지도/대륙
- 지도에 여행 경보 수준을 색깔로 표기
- 지도에 커서를 올렸을 때 국가 이름 및 여행 경보 수준 표기
- 대륙을 선택하면 해당 대륙을 확대하여 제공
- 대륙은 유럽, 아시아/중동, 미대륙, 오세아니아, 아프리카로 구분
- 나라를 검색하면 해당 국가 페이지로 이동
- 지도를 클릭하면 해당 국가 페이지로 이동

3. (메인페이지) 여행 안전 점수
- 데이터 분석을 통해 산출한 여행 안전 점수 표기
- 여행 안전 점수가 높은 순서대로 3개국 정보를 제공
- 순위, 나라명, 점수, 대륙, 안전점수 등 세부 정보를 표기
- 해당 영역을 클릭하면 국가 페이지로 이동

4. (메인페이지) 코로나 감염자 테이블 제공
- 대륙별 확진자 수, 백신 접종률 시각화 
- 국가별 확진자, 사망자, 회복자, 치명률(%), 회복률(%), 100만 명당 발생률, 1차 및 2차 접종률 테이블 제공
- 대륙을 선택하면 각 대륙에 해당하는 국가들만 표기

5. (국가페이지) 국가별 관련 정보 제공
- 데이터 분석을 통해 산출한 여행 안전 점수 표기
- 코로나 누적 통계, 코로나 신규 통계 제공
- 1, 2차 백신 접종률 시각화
- 대사관 바로가기 : 클릭 시 해당 재외공관 홈페이지로 이동
- 환율 정보 및 환율 계산기 제공 : 해당 국가의 환율정보가 없을 시에는 미국 달러 환율을 제공 

6. (국가페이지) 국가별 입국자 조치 정보 제공
- 여행 관련 정보들 볼 수 있으며 전체 정보, 요약 정보를 선택할 수 있는 기능
- 요약 정보란에는 필요 서류, 입국 관련, 격리 관련 그리고 비자 관련 정보를 세분화하여 제공 

7. (국가페이지) 사용자 공유게시판
- 사용자 간 정보 공유와 소통을 위한 댓글 기능과 중첩 댓글 기능
- 중첩 댓글 목록은 클릭 시에만 제공
- 사용자는 댓글 작성 시 닉네임, 비밀번호를 자유롭게 기입
- 댓글은 작성 시간을 기준으로 최신순으로 표기
- 댓글 수정 및 삭제기능은 사용자가 댓글 작성 시 기입했던 비밀번호를 입력해야 제공
- 사용자가 댓글 작성, 수정 및 삭제를 요청하면 성공/실패 여부를 알림으로 제공

7. (메인페이지) 최하단 카피라이트
- 회사 정보와 이용약관 등 안내 

----

## 스크린샷
**1. 지도**
![코알람1](https://user-images.githubusercontent.com/70123707/156512010-5a342662-7578-4fe4-804b-77693959b736.png)
**2. 코로나 그래프, 차트**
![코알람3](https://user-images.githubusercontent.com/70123707/156512241-7ad5c5db-caca-495f-afd7-4bca7957c2f2.png)
![코알람4](https://user-images.githubusercontent.com/70123707/156512264-83aea1f9-18b8-4836-9ff7-c476d6f14f5f.png)
**3. 국가별 페이지 예시1 >>여행관련 사항**
![코알람5](https://user-images.githubusercontent.com/70123707/156512333-b1913113-460a-404e-8545-5308a26e5f5d.png)

**4. 국가별 페이지 예시2 >>입국조치 요약**
![코알람6](https://user-images.githubusercontent.com/70123707/156512392-b5ada821-27ba-4227-81fd-5d37d089a9b2.png)
![코알람7](https://user-images.githubusercontent.com/70123707/156512515-5f82703f-9958-4de6-9e77-87610fba0246.png)
