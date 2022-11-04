import json
import requests
import os


url = os.environ['email_trigger']

headers = {'Content-Type': 'application/json'}

def send_email(message, resource, function_name):
    names = ', '.join(function_name)
    data = json.dumps({
    "message":message,
    "resource":resource,
    "functionName":names
    })
    requests.request("POST", url, headers=headers, data=data)