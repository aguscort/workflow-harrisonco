
import json
import requests
import urllib.parse
import re

# PARAMETERS 
input_data = { 'api_token': '' }
# /PARAMETERS 

# Pipedrive
def get_objects(object, api_token, start=0):
    url = 'https://api.pipedrive.com/v1/' + str(object) +  '?start=' + str(start) + '&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    print(req)
    if req['success']:
        if req['additional_data']['pagination']['more_items_in_collection']: 
            return  req['data'], req['additional_data']['pagination']['next_start'], req['additional_data']['pagination']['more_items_in_collection']
        else:
            return  req['data'], None, req['additional_data']['pagination']['more_items_in_collection']
    else:
        return False, None, None

def get_object(object, api_token, id):
    url = 'https://api.pipedrive.com/v1/' + str(object) +  '/' + str(id) + '?api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
       return  None

def get_organizations(api_token, start=0):
    return get_objects("organizations", api_token, start)

def get_organization_by_name(api_token, name):
    return get_objects("", api_token, name)
    url = 'https://api.pipedrive.com/v1/organization/find?term=' + str(name) +  '&start=' + str(start) + '&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
       return  None    

def get_organizational_field(api_token, id):
    return get_object("organizationFields", api_token, id)

def get_persons(api_token, start=0):
    return get_objects("persons", api_token, start)

def get_pipelines(api_token, start=0):
    return get_objects("pipelines", api_token, start)

def get_pipeline (api_token, id):
    return get_object("pipelines", api_token, id)

def get_stages(api_token, start=0):    
    return get_objects("stages", api_token, start)

def get_deals(api_token, start=0):
    return get_objects("deals", api_token, start)

# Airtable
def getItems(offset = None):
    req = ''
    if offset:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer keyYk3nnO04dbLGaT"}, params={"offset":offset}).json()
    else:
        req = requests.get('https://api.airtable.com/v0/appFufkqfl9yZNU5b/SKU%20List', headers={"Authorization":"Bearer keyYk3nnO04dbLGaT"},).json()
    try:
        if req['offset']:
            return req['records'], req['offset']
    except:
        return req['records'], None




#print(get_organizations(input_data['api_token']))
#print(get_organizational_field(input_data['api_token'], '4040'))
#print(get_pipelines(input_data['api_token']))
#print(get_stages(input_data['api_token']))
print(get_deals(input_data['api_token']))


output = [{'project_gid': 1, 'gid': 2, 'go_agead' : 'True'}]