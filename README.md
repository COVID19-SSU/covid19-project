# COVID-19 Project
Store and Analyze data for COVID-19.

Table of contents
=================
<!--ts-->
   * [Result](#Result)
   * [Requirement](#Requirement)
   * [Installation](#Build--Installation)
   * [Open Data](#open-data)
   * [Run](#run)
<!--te-->

Result
=======
* 코로나 실시간 현황판
  * 3월1일 ~ 오늘까지의 데이터

![date_change_](https://user-images.githubusercontent.com/55729930/92361595-90972880-f129-11ea-918c-7aa35ae12ab0.gif)


* 당일 지역별 확진자, 사망자, 격리해제 인원
* 날짜별 검사결과 그래프
* 날짜별 확진자 증가 추이 그래프
![preview_](https://user-images.githubusercontent.com/55729930/92361544-7b21fe80-f129-11ea-87b4-f4b82b83468d.gif)

* 연령대별 성별 감염자 그래프 (예정)

Requirement
=======

Installation
=======
    $ git clone https://github.com/COVID19-SSU/covid19-project.git
Open Data
=======
* 공공 데이터 포털 (https://data.go.kr/)
  * 보건복지부_코로나19 감염_현황
  * 보건복지부_코로나19 시·도발생_현황
  * 보건복지부_코로나19 연령별·성별감염_현황

Run
=======
* crawling
  * 보건복지부 코로나19 데이터(3월1일~오늘)를 크롤링하여 elasticsearch에 추가
  

         $ python covid19-project/covid19_infection_city/crawling_covid19_infection_city.py
         $ python covid19-project/covid19_infection_status/crawling_covid19_infection_status.py
    
* update
  * 기존 데이터에 보건복지부 코로나19 데이터(오늘)를 elasticsearch에 업데이트
  
        $ python covid19-project/covid19_infection_city/update_covid19_infection_city.py
        $ python covid19-project/covid19_infection_status/update_covid19_infection_status.py
    
* Task scheduler(cron) (예정)
  * 매일 정오(12:00PM)에 데이터 업데이트 프로그램 실행 예약
