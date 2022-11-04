import requests
import json
import os
from .tokengen import get_token
from .logicapp import send_email

#message to email if exception is triggered
message = "Something went wrong while executing the Azure Function Dynamic Monitor"

def get_resources():

  #generate a token, authoriazation to list resources
  new_token = get_token()
  token = 'Bearer ' + new_token
  subscription_id = os.environ['subscriptionId']

  #filter the resources by tagName equals and tagvalue eq
  filter_tag = os.environ['filter_by']
  url = f'https://management.azure.com/subscriptions/{subscription_id}/resources?$filter={filter_tag}&api-version=2021-04-01'

  payload={}
  headers = {
    'Authorization': token
  }

  #list resources and convert to json
  response_apps = requests.request("GET", url, headers=headers, data=payload)
  rjson_apps = response_apps.json()

  #get the path to the resource group
  #remove the app name, to make it generic (split the string at the last /, keep the first part after split)
  url_path = rjson_apps['value'][0]['id'].rsplit('/',1)[0]

  url = f'https://management.azure.com{url_path}/'


  #a function exists within a function app
  #get the names of function apps
  az_function_app_names = []
  for i in range(0, len(rjson_apps['value'])):
    try:
      az_function_app_names.append(rjson_apps['value'][i]['name'])
    except:
      send_email(message, url_path.split('/providers')[0], '')

  function_names = []
  #list functions for all function apps
  #store the names of the functions, will be used for query
  for app_name in az_function_app_names:
    function_url = f'{url}{app_name}/functions?api-version=2022-03-01'
    response_function = response_apps = requests.request("GET", function_url, headers=headers, data=payload)
    rjson_function = response_function.json()
    function_names.append(rjson_function['value'][0]['properties']['name'])

  return function_names, url_path