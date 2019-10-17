#Need to install requests package for python
#easy_install requests
import requests

# Set the request parameters
url = 'https://dev79112.service-now.com/api/now/table/kb_knowledge?sysparm_limit=10'

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
print(data)