# COVID-19 Project
Visualize and Analyze data for COVID-19.

Table of contents
=================
<!--ts-->
   * [Result](#Result)
   * [Requirement](#Requirement)
   * [Installation](#Installation)
   * [Run](#run)
   * [Open Data](#open-data)
<!--te-->

Result
=======
* 코로나 실시간 현황판
    * 당일 지역별 확진자, 사망자, 격리해제 인원
    * 날짜별 검사결과 그래프
    * 날짜별 확진자 증가 추이 그래프
![preview_](https://user-images.githubusercontent.com/55729930/92361544-7b21fe80-f129-11ea-87b4-f4b82b83468d.gif)
    * 성별 연령별 확진자 비율 그래프
![covid_board - Kibana](https://user-images.githubusercontent.com/55729930/92398418-7bd78680-f163-11ea-9cb8-6a72bf165737.png)

Requirement
=======
```
Python >= 3.0
```

Installation
=======
```sh
$ git clone https://github.com/COVID19-SSU/covid19-project.git
```
```sh
$ sudo docker-compose up
```
```sh
$ pip3 install -r requirements.txt
```

Run
=======
* crawling
  * 보건복지부 코로나19 데이터(3월1일 ~ 오늘)를 크롤링하여 elasticsearch에 추가
    ```shell script
    $ python3 run
    ```
    
* update
  * 기존 데이터에 보건복지부 코로나19 데이터(입력날짜)를 크롤링하여 elasticsearch에 업데이트
  * 업데이트할 날짜 구간을 선택
    ```shell script
    $ python3 run                       # 오늘의 데이터 크롤링
    $ python3 run 20200606              # 2020년 6월 6일의 데이터 크롤링
    $ python3 run 20200606 20200707     # 2020년 6월 6일 ~ 2020년 7월 7일의 데이터 크롤링
    ```
        
* add Task scheduler(cron)
  * 매일 12:00(PM)에 오늘 데이터 업데이트가 실행되도록 해당 작업 crontab에 등록 (작업 환경에 맞추어 절대 경로 수정 해줘야 함)  
    ```shell script
    $ echo -e "0 12 * * * python3 ~/covid19-project/covid19_infection_status/update_covid19_infection_status.py\n0 12 * * * python3 ~/covid19-project/covid19_infection_city/update_covid19_infection_city.py" | crontab
    ```

* Dashboard
  * Open http://localhost:5601  
  * Click `Management` tab  
  * Import [Kibana dashboard](https://github.com/COVID19-SSU/covid19-project/dashboard/export.ndjson)
  * Create Index pattern
  * Go to `Dashboard` tab

Open Data
=======
* 공공 데이터 포털 (https://data.go.kr/)
  * 보건복지부_코로나19 감염_현황
  * 보건복지부_코로나19 시·도발생_현황
  * 보건복지부_코로나19 연령별·성별감염_현황
