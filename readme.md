## [🐨회의록](https://yeardream-gitlab.elice.io/yeardream-project/project-6/coalarm/-/wikis/home#coalarm-%ED%9A%8C%EC%9D%98%EB%A1%9D) &emsp; [🥌마일스톤](https://yeardream-gitlab.elice.io/yeardream-project/project-6/coalarm/-/milestones)&emsp; [📑기획서](https://yeardream-gitlab.elice.io/yeardream-project/project-6/project-template)

# Coalarm
  
<img src="./logo.png" width="250px" height="150px" title="Github_Logo"/>


## 프로젝트 구성 안내

## 1. 프로젝트 소개
**어떠한 데이터셋와 도구 및 기술을 사용했는지에 대한 설명과 유저에게 보이는 웹서비스에 대한 소개**
* 프로젝트와 참고 모델 : [coronaboard사이트](https://coronaboard.kr/)

* 국가별 코로나 상황 데이터

* 국가별 백신 접종 현황 데이터

* 국가별 입국조치 데이터 : [외교부_국가별_한국발 입국자 조치](https://www.data.go.kr/data/15085787/openapi.do) ,[해외입국자 조치](https://www.data.go.kr/data/15085787/openapi.do)

* 사용한 언어: HTML/CSS, Javascript, python, mysql , aws 

* 사용된 라이브러리 : flask, beautifulsoup, jQuery, Selenium, geochart, re

* 협업툴 : [oneNote](https://1drv.ms/u/s!AvpSXISNxRLLhBWCvTHyI14K5ZAr?e=2FBl2U)

## 2. 프로젝트 목표
  - 국내 방역 체계가 단계적 일상 회복 '위드 코로나'로 바뀌면서 어려웠던 해외 여행에 대한 관심이 높아졌다. 나라 마다 방역 정책이 다르고 필요한 정보를 제공하는 곳도 다양하기 때문에 여행하고자 하는 나라의 정보를 여러 곳에서 수집하여야 하는 불편함이 있다. 이를 해결하기 위해서 사용자들이 원하는 나라의 여행정보를 쉽게 파악할 수 있고, 데이터를 기반으로 안전하게 여행할 수 있는 국가를 추천하는 서비스를 개발하고자 한다.


## 3. 프로젝트 기능 설명

** 해외여행에 필요한 코로나 바이러스 관련 정보를 제공한다. **

* 외교부에서 제공하는 API 활용하여 국가별 코로나 현황을 보여주고, 여행에 필요한 정보를 제공한다.

* 출장, 유학, 여행을 준비는데 필요한 실질적인 정보들을 효과적으로 제공한다.

* 주요 기능
    - 국가별로 코로나 바이러스의 발생 현황을 시각적으로 보여준다.
    - 지도에 인구대비 확진자 수를 색깔로 표시한다.
    - 해당 국가의 코로나 관련 조치를 한눈에 파악할 수 있도록 한다.
* 부가기능
    - 국가별 백신 접종률
    - 국각별 자가격리 기간/ 입국 시 지참서류/비자관련 체류기간 정보
    - ~~개인 정보 입력했을 때 입국 가능 여부 알려주기~~
    - ~~조건 검색(필터) 기능~~
    - 지금 여행하기 좋은 국가 추천 (갑자기 확진자 수가 낮아진 국가 등)
    - 해당 국가의 관광지 추천
    - 비행기 예매, 숙박 관련 예매 사이트 연동
    - ~~다양한 언어 지원~~
    - 결과 공유
    - 댓글 기능 (여행자들의 커뮤니티)
    - 환율 정보



## 4. 프로젝트 팀원 역할 분담
| 이름    | 담당 역할         | 내용                            |  Task Part|
| ------ | ------            | -----                           | ------    |
| **김태윤**  | 팀 리더           | 의견조율, 동기부여, 방향제시      | Front-end,Back-end 연동 |
| **최웅수**  | oneNote 리더     |  oneNote 관리, 오류 및 이슈해결  | Back-end |
| **정준호**  | 일정관리 리더      |  일정 관리, 공유, 더블체크       | Back-end  |
| **박병규**  | 회의록 리더        |  oneNote 화의록 작성 및 관리     | Back-end  |
| **유승아**  | 현장 리더          |  현장에서 처리가능한 업무 수행    | Back-end  |
| **박용석**  | gitLap 리더        | gitLap 관리, 오류 및 이슈해결    | Front-end |


## 5. FAQ
  - 자주 받는 질문 정리
