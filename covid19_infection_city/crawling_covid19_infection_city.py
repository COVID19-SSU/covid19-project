from bs4 import BeautifulSoup
import requests
import json
import xmltodict
from datetime import datetime
from elasticsearch import Elasticsearch
import os


# 문자열 변경 함수 (str.replace의 반대버전)
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


# 공공 데이터 센터의 covid19 감염자 지역현황 집계 첫날부터 오늘까지의 감염 현황 데이터를 크롤링하여 엘라스틱 서치에 삽입

# 코로나 집계 첫날부터 오늘까지의 감염자 지역 데이터 받기

update = '?serviceKey=MMq1VsRlz5qKvsdKDrvMavJB5rGdJOA8JGKgyojceXcL5tj6MJtzG21jN30ke9OOHZI%2FsQEwftRprl%2FQjcE2bg%3D%3D&pageNo=1&numOfRows=10&startCreateDt=20200120&endCreateDt=' + datetime.today().strftime(
    "%Y%m%d") + '&'
url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson' + update

# xml데이터를 파싱 후 json형태로 변환
req = requests.get(url)
html = req.text
jsontxt = json.dumps(xmltodict.parse(html), indent=4)
root_json = json.loads(jsontxt)

# 매핑 불러오기
with open("mapping_covid19_infection_city.json", 'r') as f:
    mapping = json.load(f)

# 오늘까지의 doc을 dict형태로 변환 후 doc_list에 추가
# 공공api에서 제공하는 데이터 중 기준 날짜를 의미하는 문자열을 수정하여 date형식으로 변경
doc_list = []
for j in root_json['response']['body']['items']['item']:
    doc = {}
    for i in j:
        doc[i] = j[i]
    doc['stdDay'] = doc['stdDay'][:doc['stdDay'].index('일')]
    doc['stdDay'] = doc['stdDay'].replace('년 ', '-').replace('월 ', '-')
    if len(doc['stdDay'].split('-')[1]) < 2:
        doc['stdDay'] = doc['stdDay'].replace(doc['stdDay'].split('-')[1], '0' + doc['stdDay'].split('-')[1], 1)
    if len(doc['stdDay'].split('-')[2]) < 2:
        doc['stdDay'] = rreplace(doc['stdDay'], doc['stdDay'].split('-')[2], '0' + doc['stdDay'].split('-')[2], 1)
    doc_list.append(doc)

# 엘라스틱 서치에 doc_list추가
es = Elasticsearch('localhost:9200')
index = "covid19_infection_city"
es.indices.create(index=index, body=mapping)
for i in doc_list:
    es.index(index=index, doc_type="_doc", body=i)
