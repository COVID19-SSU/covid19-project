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
   * [Schema Explanation](#Schema-Explanation)
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
Save `status_of_infected_person`, `infected_people_by_city`, `age_gender_of_infected_person` data from `OPEN api` in `elasticsearch` and update daily
* crawling
  * 보건복지부 코로나19 데이터(3월1일~오늘)를 크롤링하여 elasticsearch에 추가
    ```shell script
    $ python3 run.py
    ```
    
* update
  * 기존 데이터에 보건복지부 코로나19 데이터(입력날짜)를 크롤링하여 elasticsearch에 업데이트
  * 업데이트할 날짜 구간을 선택

    ```shell script
    $ python3 run.py -d                       # 오늘의 데이터 크롤링
    $ python3 run.py -d 20200606              # 2020년 6월 6일의 데이터 크롤링
    $ python3 run.py -d 20200606 20200707     # 2020년 6월 6일 ~ 2020년 7월 7일의 데이터 크롤링
    ```
        
* add Task scheduler(cron)
  * 매일 12:00(PM)에 오늘 데이터 업데이트가 실행되도록 해당 작업 crontab에 등록 (작업 환경에 맞추어 절대 경로 수정 해줘야 함)  
    ```shell script
    $ echo -e "0 12 * * * python3 ~/covid19-project/run.py -d" | crontab
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
  
Schema Explanation
=======
* status_of_infected_person

|Item name|Item Description|Sample|
|:----:|:----:|:----:|
|SEQ|게시글번호(국내 시도별 발생현황 고유값)|74|
|STATE_DT|기준일|20200315|
|STATE_TIME|기준시간|00:00|
|DECIDE_CNT|확진자 수|8162|
|CLEAR_CNT|격리해제 수|834|
|EXAM_CNT|검사진행 수|16272|
|DEATH_CNT|사망자 수|75|
|CARE_CNT|치료중 환자 수|7253|
|RESUTL_NEG_CNT|결과 음성 수|243778|
|ACC_EXAM_CNT|누적 검사 수|268212|
|ACC_EXAM_COMP_CNT|누적 검사 완료 수|251940|
|ACC_DEF_RATE|누적 확진률|3.2396602365|
|CREATE_DT|등록일|2020-03-15|
|UPDATE_DT|수정일시분초|null|

* infected_people_by_city

|Item name|Item Description|Sample|
|:----:|:----:|:----:|
|SEQ|게시글번호(국내 시도별 발생현황 고유값)|130|
|CREATE_DT|등록일시분초|2020-04-10 11:15:59.026|
|gubun|시도명(한글)|제주|
|gubunCn|시도명(중국어)|济州|
|gubunEn|시도명(영어)|Jeju|
|deathCnt|사망자 수|14|
|defCnt|감염자 수|561|
|INC_DEC|전일대비 증감 수|39|
|ISOL_CLEAR_CNT|격리 해제 수|6973|
|QUR_RATE|10만명당 발생률|20.10|
|STD_DAY|기준일시|2020-03-13|
|UPDATE_DT|수정일시분초|null|

* age_gender_of_infected_person

|Item name|Item Description|Sample|
|:----:|:----:|:----:|
|SEQ|게시글번호(성별, 연령별)|134|
|GUBUN|구분(성별, 연령별)|남성(성별), 10-19(연령별)|
|CONF_CASE|확진자 수|132|
|CONF_CASE_RATE|확진률|1.25|
|DEATH|사망자|0|
|DEATH_RATE|사망률|0.00|
|CRITICAL_RATE|치명률|0.00|
|CREATE_DT|등록일|2020-03-15|
|UPDATE_DT|수정일시분초|null|
  
