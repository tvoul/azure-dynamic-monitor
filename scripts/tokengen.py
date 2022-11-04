import requests
import json
import os

#RBAC info
clientId = os.environ['rbac_appId']
clientSecret = os.environ['rbac_password']
tenantId = os.environ['rbac_tenant']
resource = 'https://management.azure.com/'
baseUrl = 'https://login.microsoftonline.com/'

url = baseUrl + tenantId + '/oauth2/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

body = {
    'mode':'urlencoded',
    'grant_type':'client_credentials',
    'client_id':clientId,
    'client_secret':clientSecret,
    'resource':resource
}

def get_token():
    response = requests.request("POST", url, headers=headers, data=body)
    rjson = response.json()
    bearerToken = rjson['access_token']
    return bearerToken