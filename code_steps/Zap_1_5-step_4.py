import json
import requests
import urllib.parse
import re

# PARAMETERS 
input_data = { 'type_person':	'',
    'person_id':	'',
    'api_token' : ''}
# /PARAMETERS 

def get_object(object, api_token, id):
    url = 'https://api.pipedrive.com/v1/' + str(object) +  '/' + str(id) + '?start=0&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
        return  None

def get_person_field(api_token, id):
    return get_object("personFields", api_token, id)

def get_person(api_token, id):
    return get_object("persons", api_token, id)

try:
    person_type_dict = {}
    status = {}
    type_name = []
    person_type_dict = get_person_field(input_data['api_token'], '9071') 
    for item in person_type_dict['options']:
        status[item['id']] = item['label']
    if input_data['type_person'].find(",") != -1:
        types = input_data['type_person'].split(",")
        for i in types:
            type_name.append(str(status[int(i)]))                
        output = [{'types': ",".join(list(set(type_name)))}]
    else:
        output = [{'types': str(status[int(input_data['type_person'])])}]
except:
    output = [{'types': ""}]
