from bs4 import BeautifulSoup
import requests
import json
import xmltodict
from datetime import datetime
from elasticsearch import Elasticsearch

# 공공 데이터 센터의 covid19 감염현황의 오늘자 데이터를 크롤링하여 엘라스틱 서치에 삽입(업데이트)

# 코로나 집계 첫날부터 오늘까지의 데이터 받기
update = '?serviceKey=MMq1VsRlz5qKvsdKDrvMavJB5rGdJOA8JGKgyojceXcL5tj6MJtzG21jN30ke9OOHZI%2FsQEwftRprl%2FQjcE2bg%3D%3D&pageNo=1&numOfRows=10&startCreateDt='+datetime.today().strftime("%Y%m%d")+'&'
url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson'+update

# xml데이터를 파싱 후 json형태로 변환
req=requests.get(url)
html=req.text
soup=BeautifulSoup(html, 'xml')
jsontxt=json.dumps(xmltodict.parse(html), indent=4)
root_json = json.loads(jsontxt)
print(root_json['response']['body'])
# 오늘 doc을 dict형태로 변환
doc_list =[]
for i in root_json['response']['body']['items']['item']:
   #print(i,"---")
   doc_list.append(i)
for doc in doc_list:
   doc['createDt']=doc['createDt'][0:10]
# 엘라스틱 서치에 doc추가
es = Elasticsearch('localhost:9200')
index="covid19_infection_GenAge"
es.index(index=index,doc_type="_doc",body=doc)