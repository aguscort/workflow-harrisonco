import json
import requests
import urllib.parse
import re

# PARAMETERS 
input_data = { 'api_token': 'b18c3a24625a6da23b46bf2c10f7d26780bdda82', 'name' : 'Sand Cloud' , 'type' : 'Private Equity,Growth Equity,Venture Capital,Family Office'}
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

count = 0
all_organizations = []
all_organizations, next_bundle, more = get_organizations(input_data['api_token'],700}
while more and more != "None":
    more_organizations, next_bundle, more = get_organizations(input_data['api_token'], next_bundle)
    all_organizations.extend(more_organizations)    
print (len(all_organizations))

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
    print(item)
    if item['label'] in input_data['type'].split(","):    
        valid_status[item['id']] = item['label']       
organizational_field_key = company_type_dict['key']
print(valid_status)

for o in all_organizations:
    go_ahead = 'False'   
    print("--------")
    #print(o['id'])     
    # Get all the organization info       
    org_det = get_organization(input_data['api_token'], str(o['id']))
    if org_det[organizational_field_key] in valid_status:
        go_ahead = 'True'
        company_type = org_det[organizational_field_key]
    else:
        go_ahead = 'False'
        company_type = None
    if org_det[organizational_field_key] is not None:
        o_status = org_det[organizational_field_key].split(",") # it can contain several values    
        if "211" in o_status:
            print(o['name'])
            for s in o_status:
                print(o_status)
                if s in valid_status:
                    go_ahead = 'True'
                    company_type = valid_status[org_det[organizational_field_key]]
                    print("Status OK" + s)
                    stage_id  = get_deal_by_id(input_data['api_token'],org_det ['last_activity']['deal_id'] )['stage_id']
                    pipeline_id = get_stage_by_id(input_data['api_token'], stage_id )['pipeline_id'] 


    #             #num_deals, start, more = get_deals_in_pipeline(input_data['api_token'], )
    #             company_deals = ''
    #             portfolio = ''
    #             portfolio_sectors = ''
    #             num_deals = ''

    #             # print(field['options'])
    #             output = {'go_ahead': go_ahead,  'company_type' : company_type, 'pipeline' : get_pipeline_by_id(input_data['api_token'], pipeline_id)['name'], 'company_deals' : company_deals, 'num_deals' :  num_deals, 'portfolio' : portfolio , 'portfolio_sectors' : portfolio_sectors}
    #         else:          
    #             put = {'go_ahead': 'False',  'company_type' : 'None', 'pipeline' : 'None', 'company_deals' : 'None', 'num_deals' :  'None', 'portfolio' : 'None' , 'portfolio_sectors' : 'None'}
    #print(output)                