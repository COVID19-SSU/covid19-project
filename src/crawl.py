from src import func
from conf import api_config
from conf import constants

# 문자열 변경 함수 (str.replace의 반대버전)
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def crawl_city():
    url = api_config.COVID_CITY_URL + api_config.COVID_KEY_ALL
    json_txt=func.xml_to_json(url)
    doc_list = []
    for j in json_txt['response']['body']['items']['item']:
        doc = {}
        for i in j:
            doc[i] = j[i]
        doc['stdDay'] = doc['stdDay'][:doc['stdDay'].index('일')]
        doc['stdDay'] = doc['stdDay'].replace('년 ', '-').replace('월 ', '-')
        if len(doc['stdDay'].split('-')[1]) < 2:
            doc['stdDay'] = doc['stdDay'].replace(doc['stdDay'].split('-')[1], '0' + doc['stdDay'].split('-')[1], 1)
        if len(doc['stdDay'].split('-')[2]) < 2:
            doc['stdDay'] = rreplace(doc['stdDay'], doc['stdDay'].split('-')[2], '0' + doc['stdDay'].split('-')[2], 1)
        doc = func.change_region_name(doc)
        doc_list.append(doc) 
    func.put_es_all(constants.CITY, doc_list)

def crawl_city_date(start,end):
    url = api_config.COVID_CITY_URL + api_config.COVID_KEY_START + start + api_config.COVID_KEY_END + end + '&'
    json_txt=func.xml_to_json(url)
    doc_list = []
    for j in json_txt['response']['body']['items']['item']:
        doc = {}
        for i in j:
            doc[i] = j[i]
        doc['stdDay'] = doc['stdDay'][:doc['stdDay'].index('일')]
        doc['stdDay'] = doc['stdDay'].replace('년 ', '-').replace('월 ', '-')
        if len(doc['stdDay'].split('-')[1]) < 2:
            doc['stdDay'] = doc['stdDay'].replace(doc['stdDay'].split('-')[1], '0' + doc['stdDay'].split('-')[1], 1)
        if len(doc['stdDay'].split('-')[2]) < 2:
            doc['stdDay'] = rreplace(doc['stdDay'], doc['stdDay'].split('-')[2], '0' + doc['stdDay'].split('-')[2], 1)
        doc = func.change_region_name(doc)
        doc_list.append(doc)
    
    func.put_es(constants.CITY, doc_list)

def crawl_status():
    url = api_config.COVID_STATUS_URL + api_config.COVID_KEY_ALL
    json_txt=func.xml_to_json(url)
    doc_list = []
    for j in json_txt['response']['body']['items']['item']:
        doc = {}
        for i in j:
            doc[i] = j[i]
        doc['createDt'] = doc['createDt'][0:10]
        doc_list.append(doc)
    func.put_es_all(constants.STATUS, doc_list)

def crawl_status_date(start, end):
    url = api_config.COVID_STATUS_URL + api_config.COVID_KEY_START + start + api_config.COVID_KEY_END + end + '&'
    json_txt=func.xml_to_json(url)
    doc_list = []
    if start == end :
        doc = {}
        for i in json_txt['response']['body']['items']['item']:
            doc[i] = json_txt['response']['body']['items']['item'][i]
        doc['createDt'] = doc['createDt'][0:10]
        doc_list.append(doc)
    else :
        for j in json_txt['response']['body']['items']['item']:
            doc = {}
            for i in j:
                doc[i] = j[i]
            doc['createDt'] = doc['createDt'][0:10]
            doc_list.append(doc)

    func.put_es(constants.STATUS, doc_list)

def crawl_gen_age():
    url = api_config.COVID_GEN_AGE_URL + api_config.COVID_KEY_ALL
    json_txt=func.xml_to_json(url)
    doc_list=[]
    for i in json_txt['response']['body']['items']['item']:
        doc_list.append(i)
    for doc in doc_list:
        doc['createDt']=doc['createDt'][0:10]
    func.put_es_all(constants.GENAGE, doc_list)

def crawl_gen_age_date(start, end):
    url = api_config.COVID_GEN_AGE_URL + api_config.COVID_KEY_START + start + api_config.COVID_KEY_END + end + '&'
    json_txt=func.xml_to_json(url)
    doc_list=[]
    for i in json_txt['response']['body']['items']['item']:
        doc_list.append(i)
    for doc in doc_list:
        doc['createDt']=doc['createDt'][0:10]
    func.put_es(constants.GENAGE, doc_list)
