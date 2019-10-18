import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Senior_Design_Table')
short_description = ''
roles = ''
wiki = ''
link = ''
text = ''

table.put_item(
    Item={'short_description':short_description,
          'roles': roles,
           'wiki': wiki,
           'link': link,
            'text': text}
)
