import requests
import json
import xmltodict
from elasticsearch import Elasticsearch
from conf import constants


def change_region_name(doc):
    if doc['gubunEn'] == 'Busan':
        doc['gubunEn'] = 'Busan'
        doc['gubun'] = '부산광역시'
    elif doc['gubunEn'] == 'Chungcheongbuk-do':
        doc['gubunEn'] = 'North Chungcheong Province'
        doc['gubun'] = '충청북도'
    elif doc['gubunEn'] == 'Chungcheongnam-do':
        doc['gubunEn'] = 'South Chungcheong Province'
        doc['gubun'] = '충청남도'
    elif doc['gubunEn'] == 'Daegu':
        doc['gubunEn'] = 'Daegu'
        doc['gubun'] = '대구광역시'
    elif doc['gubunEn'] == 'Daejeon':
        doc['gubunEn'] = 'Daejeon'
        doc['gubun'] = '대전광역시'
    elif doc['gubunEn'] == 'Gangwon-do':
        doc['gubunEn'] = 'Gangwon Province'
        doc['gubun'] = '강원도'
    elif doc['gubunEn'] == 'Gwangju':
        doc['gubunEn'] = 'Gwangju'
        doc['gubun'] = '광주광역시'
    elif doc['gubunEn'] == 'Gyeonggi-do':
        doc['gubunEn'] = 'Gyeonggi Province'
        doc['gubun'] = '경기도'
    elif doc['gubunEn'] == 'Gyeongsangbuk-do':
        doc['gubunEn'] = 'North Gyeongsang Province'
        doc['gubun'] = '경상북도'
    elif doc['gubunEn'] == 'Gyeongsangnam-do':
        doc['gubunEn'] = 'South Gyeongsang Province'
        doc['gubun'] = '경상남도'
    elif doc['gubunEn'] == 'Incheon':
        doc['gubunEn'] = 'Incheon'
        doc['gubun'] = '인천광역시'
    elif doc['gubunEn'] == 'Jeju':
        doc['gubunEn'] = 'Jeju'
        doc['gubun'] = '제주특별자치도'
    elif doc['gubunEn'] == 'Jeollabuk-do':
        doc['gubunEn'] = 'North Jeolla Province'
        doc['gubun'] = '전라북도'
    elif doc['gubunEn'] == 'Jeollanam-do':
        doc['gubunEn'] = 'South Jeolla Province'
        doc['gubun'] = '전라남도'
    elif doc['gubunEn'] == 'Sejong':
        doc['gubunEn'] = 'Sejong City'
        doc['gubun'] = '세종특별자치시'
    elif doc['gubunEn'] == 'Seoul':
        doc['gubunEn'] = 'Seoul'
        doc['gubun'] = '서울특별시'
    elif doc['gubunEn'] == 'Ulsan':
        doc['gubunEn'] = 'Ulsan'
        doc['gubun'] = '울산광역시'

    return doc


def xml_to_json(addr):
    req = requests.get(addr)
    html = req.text
    jsontxt = json.dumps(xmltodict.parse(html), indent=4)
    root_json = json.loads(jsontxt)
    return root_json


# 문자열 변경 함수 (str.replace의 반대버전)
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def put_es_all(type, doc_list):
    if type == constants.Type.CITY:
        index = "covid19_infected_people_by_city"
        with open("mapping/mapping_city.json", 'r') as f:
            mapping = json.load(f)
    elif type == constants.Type.GEN_AGE:
        index = "age_gender_of_infected_person"
        with open("mapping/mapping_gen_age.json", 'r') as f:
            mapping = json.load(f)
    elif type == constants.Type.STATUS:
        index = "status_of_infected_person"
        with open("mapping/mapping_status.json", 'r') as f:
            mapping = json.load(f)
    es = Elasticsearch('localhost:9200')
    es.indices.create(index=index, body=mapping)
    for i in doc_list:
        es.index(index=index, doc_type="_doc", body=i)


def put_es(type, doc_list):
    if type == constants.Type.CITY:
        index = "covid19_infected_people_by_city"
    elif type == constants.Type.GEN_AGE:
        index = "age_gender_of_infected_person"
    elif type == constants.Type.STATUS:
        index = "status_of_infected_person"
    es = Elasticsearch('localhost:9200')

    for i in doc_list:
        es.index(index=index, doc_type="_doc", body=i)
