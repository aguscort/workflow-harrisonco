import json
import requests
import urllib.parse
import re

# PARAMETERS 
input_data = { 'type':	'',
    'id' : '',
    'name':	'',
    'api_token' : ''}
# /PARAMETERS 


# Pipedrive
def get_objects(object, api_token, start=0):
    url = 'https://api.pipedrive.com/v1/' + str(object) +  '?start=' + str(start) + '&api_token=' + str(api_token)
    print(url)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        if req['additional_data']['pagination']['more_items_in_collection']: 
            return  req['data'], req['additional_data']['pagination']['next_start'], req['additional_data']['pagination']['more_items_in_collection']
        else:
            return  req['data'], None, req['additional_data']['pagination']['more_items_in_collection']
    else:
        return None, None, False
    
def get_object(object, api_token, id):
    url = 'https://api.pipedrive.com/v1/' + str(object) +  '/' + str(id) + '?start=0&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
        return  None

def get_organizations(api_token, start=0):
    return get_objects("organizations", api_token, start)

def get_organization_by_name(api_token, name, start=0):
    url = 'https://api.pipedrive.com/v1/organizations/find?term=' + urllib.parse.quote(name) +  '&start=' + str(start) + '&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
        return  None    

def get_organization(api_token, id, start=0):
    return get_object("organizations", api_token, id)

def get_organizational_field(api_token, id, start=0):    
    if id is not None:        
        return get_object("organizationFields", api_token, id)
    else:
        return None

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

def get_organization_deals(api_token, id, start=0):
    if id is not None:        
        return get_object("organizations", api_token, str(id) + "/deals")
    else:
        return None

def get_deal_by_id(api_token, id, start=0):
    if id is not None:        
        return get_object("deals", api_token, id)
    else:
        return None

def get_stage_by_id(api_token, id, start=0):    
    if id is not None:        
        return get_object("stages", api_token, id)
    else:
        return None    

def get_relationships_by_id(api_token, id, start=0):    
    url = 'https://api.pipedrive.com/v1/organizationRelationships/?org_id=' + str(id) + '&start=0&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}  
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        return req['data']
    else:
        return  None   
    
def get_pipeline_by_id(api_token, id, start=0):    
    if id is not None:        
        return get_object("pipelines", api_token, id)
    else:
        return None    


def get_deals_in_pipeline(api_token, id ,start=0):
    url = 'https://api.pipedrive.com/v1/pipelines/' + str(id) +  '/deals?start=' + str(start) + '&api_token=' + str(api_token)
    headers = {"Content-Type" :"application/json"}     
    req = requests.get(url, headers=headers ).json()
    if req['success']:
        if req['additional_data']['pagination']['more_items_in_collection']: 
            return  req['data'], req['additional_data']['pagination']['next_start'], req['additional_data']['pagination']['more_items_in_collection']
        else:
            return  req['data'], None, req['additional_data']['pagination']['more_items_in_collection']
    else:
        return None, None, False

    
deals = 0
count = 0
company_deals = ''
# Get the valid types of Organizations 
valid_status  = {}
company_type_dict = get_organizational_field(input_data['api_token'], '4040') 
for item in company_type_dict['options']:
    #print(item)
    if item['label'] in input_data['type'].split(","):    
        valid_status[item['id']] = item['label']       
organizational_field_key = company_type_dict['key']

go_ahead = 'False'   
company_name = None
company_id = None   
parent_name = None
parent_id = None
# Get all the organization info       
org_rel = get_relationships_by_id(input_data['api_token'], int(input_data['id']))
try:
    for i in org_rel:
        if str(i['rel_linked_org_id']['value']) == str(input_data['id']) and i['type'] == 'parent':
            org_det = get_organization(input_data['api_token'], int(i['rel_owner_org_id']['value'])) 
            if int(org_det[organizational_field_key]) in valid_status:               
                go_ahead = 'True'
                company_name = i['rel_linked_org_id']['name']
                company_id = i['rel_linked_org_id']['value']
                parent_id = i['rel_owner_org_id']['value']     
                parent_name = i['rel_owner_org_id']['name']     
            else:
                print('Parent not a valid Org')            
except:
    pass
                
output = {'go_ahead': go_ahead,  'company_name' : company_name, 'company_id' : company_id, 'parent_name' : parent_name, 'parent_id' : parent_id} 