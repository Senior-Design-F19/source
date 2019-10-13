import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Senior_Design_Table')
table.put_item(
    Item={'title':'Hello'}
)
