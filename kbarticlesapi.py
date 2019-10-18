#Need to install requests package for python
#easy_install requests
import boto3
import json
from boto3.dynamodb.conditions import Key
import requests

# Set the request parameters
url = 'https://dev79112.service-now.com/api/now/table/kb_knowledge'

# Set username and password
user = 'admin'
pwd = 'a9mMPOunKO3l'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
objstr = json.dumps(data)
obj = json.loads(objstr)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Senior_Design_Table')

for i in range(len(obj["result"])):
    if obj["result"][i]["text"] == "":
        table.put_item(
            Item={'short_description': obj["result"][i]["short_description"],
                'wiki': obj["result"][i]["wiki"],
                'link': obj["result"][i]["kb_category"]["link"]}
        )

    else:
            table.put_item(
            Item={'short_description': obj["result"][i]["short_description"],
                'wiki': obj["result"][i]["wiki"],
                'link': obj["result"][i]["kb_category"]["link"],
                'text': obj["result"][i]["text"]}
        )