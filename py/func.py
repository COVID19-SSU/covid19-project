from bs4 import BeautifulSoup
import requests
import json
import xmltodict
from datetime import datetime
from elasticsearch import Elasticsearch
import os
from py import conf

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



def put_es_all(type,doc_list):
    if type == conf.CITY:
        index = "covid19_infected_people_by_city"
        with open("mapping/mapping_city.json", 'r') as f:
            mapping = json.load(f)
    elif type == conf.GENAGE:
        index = "age_gender_of_infected_person"
        with open("mapping/mapping_gen&age.json", 'r') as f:
            mapping = json.load(f)
    elif type == conf.STATUS:
        index = "status_of_infected_person"
        with open("mapping/mapping_status.json", 'r') as f:
            mapping = json.load(f)
    es = Elasticsearch('localhost:9200')
    es.indices.create(index=index, body=mapping)
    for i in doc_list:
        es.index(index=index, doc_type="_doc", body=i)

def put_es(type,doc_list):
    if type == conf.CITY:
        index = "covid19_infected_people_by_city"
    elif type == conf.GENAGE:
        index = "age_gender_of_infected_person"        
    elif type == conf.STATUS:
        index = "status_of_infected_person" 
    es = Elasticsearch('localhost:9200')

    for i in doc_list:
        es.index(index=index, doc_type="_doc", body=i)




