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

# Get the pipelines
pipelines_dict = {}
pipelines, start, more = get_pipelines(input_data['api_token'])
for p in pipelines:
    try:
        if p['active']:
            pipelines_dict[p['id']] = p['name']  
    except:        
        pass  
# Get the valid types of Organizations 
valid_status  = {}
company_type_dict = get_organizational_field(input_data['api_token'], '4040') 
for item in company_type_dict['options']:
    #print(item)
    if item['label'] in input_data['type'].split(","):    
        valid_status[item['id']] = item['label']       
organizational_field_key = company_type_dict['key']
print(valid_status)

company_deals = ''
deals = 0
go_ahead = 'False'         
org_det = get_organization(input_data['api_token'], int(input_data['id']))
if org_det[organizational_field_key] in valid_status:
    go_ahead = 'True'
    company_type = org_det[organizational_field_key]
else:
    go_ahead = 'False'
    company_type = None
if org_det[organizational_field_key] is not None:
    o_status = org_det[organizational_field_key].split(",") # it can contain several values
    first_status = True
    for s in o_status:
        #print(s)
        if str(s) in ['316','315','314','214']:
            if first_status and len(company_deals) > 0:
                company_deals += ', '
                first_status = False
            company_type = valid_status[int(s)]
            print(company_type)
            print(org_det ['open_deals_count'])
            if org_det ['open_deals_count'] > 0:
                    active_deal = get_organization_deals(input_data['api_token'],str(input_data['id']))
                    for i in range(len(active_deal)):
                        if i > 0:
                            company_deals += ', '
                        print(active_deal[i]["id"])
                        print(active_deal[i]["stage_id"])
                        company_deals += active_deal[i]["title"].split(" | ")[0]  
                        deals += 1 
            go_ahead = 'True'
output = {'go_ahead': go_ahead,  'company_type' : company_type, 'company_deals' : ", ".join(set(company_deals.split(","))), 'num_deals' :  deals}    