import requests
import json
import os
import azure.functions as func
from .resources import get_resources
from .logicapp import send_email

#sends with email
message = 'The following function(s) have not returned any matching data, based on the query sent to the logs.'

#application insights
app_id = os.environ['application_insights_app_id']
api_key = os.environ['application_insights_api_key']
url = f'https://api.applicationinsights.io/v1/apps/{app_id}/query'

def main(mytimer: func.TimerRequest) -> None:

    resources = get_resources()

    #names of the functions, will be used in the query
    az_function_names = resources[0]

    #resource will be included in the email
    resource = resources[1].split('/providers')[0]

    empty_logs = [] #array to store function who's logs are empty

    for name in az_function_names:
        query = os.environ['query'] + f' and name == "{name}"'
        queryDict = json.dumps({'query': query})

        headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
        }

        data = get_data(headers, queryDict)
        if (len(data['tables'][0]['rows']) == 0):
            empty_logs.append(name)
    
    #if there are emtpy logs, send an email with the name(s) of the function(s)
    if (len(empty_logs) != 0):
        send_email(message, resource, empty_logs)

def get_data(headers, query):
  response = requests.request("POST", url, headers=headers, data=query)
  rjson = response.json()
  return rjson