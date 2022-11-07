List a group of Azure resources to retrieve the names of functions and then query application insights.
This script-set is meant to be deployed as an Azure Function timer trigger.

The idea was to make the code as flexible as possible. The Function App monitors an undefined number of functions, it starts by listing all the resources and filters them out by a specified tag name. It then has a loop that send’s a query for every function name retrieved based on the filter applied.

That way, if we wish to add a new function to monitor, we only have to tag it appropriately in Azure.
And correspondingly if a resource is removed (or even it’s tag), it will by extent also stop being monitored.

The same function we wish to monitor could have multiple tags and therefore have different queries run at different intervals.
## How it works
Generate a token to get access. \
Using Azure Resource Manager and Azure REST-API, list the resources inside a resource group. \
Filter the resources by a specified tag name. \
For every function app, make new API calls to retrieve the names of functions. \
For every function name, query application insights. If the results are empty, trigger the Logic App to send an email.

## Prerequisites
### 1. All functions are created within the same resource group.
In it's current state this script set works on a resource group scope. This could be further abstracted to a subscription level, but you would need to adjust the code yourself.

https://learn.microsoft.com/en-us/rest/api/resources/resource-groups/list \
https://learn.microsoft.com/en-us/rest/api/resources/resources/list-by-resource-group

### 2. Functions we wish to monitor have a tag which we will filter the resources by
### 3. The functions we wish to monitor are logged in the same instance of Application Insights

## Delimitations
It has only been tested for Function Apps containing one function.

# Setup

## RBAC
Using Azure CLI, create a service principal and configure its access to Azure resources. \
The generated values will be used in a later step.

````
    az login
    az ad sp create-for-rbac --role Reader --scopes SCOPE --display-name NAME
````



## Application Insights
Create an API key for Application Insights \
https://learn.microsoft.com/en-us/azure/bot-service/bot-service-resources-app-insights-keys?view=azure-bot-service-4.0

## Enviroment variables

In the Configuration of the Function App in Azure portal, add the following key-pair values as application settings. They will be read as environment variables.

### keys - values
### 1. subscriptionId - your subscriptions id
### 2. application_insights_api_key - API key
### 3. application_insights_app_id - Application ID, can be found under API access
### 4. rbac_appId - appId from RBAC created
### 5. rbac_password - password from RBAC created
### 6. rbac_tenant - tenant from RBAC created
### 7. filter_by - what you wish to filter the resource api call by
*example: tagname eq 'find-me'*
### 8. query - the query you wish to run in application insights. " 
note: " and name == 'app-name'" will be concatenated at the end of your query. \
*example query: requests| where timestamp > ago(24h)* \
*resulting query in code: requests| where timestamp > ago(24h) and name == 'app-name'*
### 9. email_trigger - url to the http triggered Logic App (or similar solution)

![Screenshot](https://user-images.githubusercontent.com/90894009/200328126-c7e4516d-26f6-4216-a360-c4c8900404bf.png)


## Logic App
Setup an http triggered Logic App, set the method to post.
Add a second step to send an email, you can use the information received to compose the email.

This is meant to be generic, so it could be used by multiple instances of the monitoring function.

#### JSON Schema
```
{
    "properties": {
        "functionName": {
            "type": "string"
        },
        "message": {
            "type": "string"
        },
        "resource": {
            "type": "string"
        }
    },
    "type": "object"
}
```

![Screenshot2](https://user-images.githubusercontent.com/90894009/200333773-642ef27a-d847-47a7-8b4f-e3ffc3339e4d.png)

