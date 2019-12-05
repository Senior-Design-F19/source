import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import re
#import nltk
#from nltk.corpus import stopwords
#import requests

dynamo = boto3.client('dynamodb')

def search(phrase):
    # remove punctuation and special characters
    phrase = re.sub('[^A-Za-z0-9 ]+', '', phrase)
    
    # remove stopwords
    with open('english') as f:  
        stopwords = [word.strip() for word in f]    # get a list of all stopwords
    
    phrase = ' '.join([w for w in phrase.lower().split() if w not in stopwords]) #remove all stopwords from phrase
    
    # split phrase into words 
    phraseList = re.sub("[^\w]", " ",  phrase).split()
    
    # stemming can go here

    # find all aritcles related to each word 
    response = scan_table()     # get all rows from table 
    allShortDescriptions = []
    for i in response['Items']:
        allShortDescriptions.append(i['short_description']) # get a list of all short descriptions
    
    matches = []   
    for k in phraseList:
        for i in allShortDescriptions:
            if i.lower().find(k.lower()) != -1:
               matches.append(i)    # if word is found in title then add title to list 
                
    # find intersection of articles by checking for duplicates 
    results = pruneList(matches,phraseList) 
    results = sorted(results.items(), key=lambda x: x[1], reverse=True) # sort results based on weight
    
    response = {}
    res = ""
            
    i = 0
    for key,value in results: #print actual results
        res = query_table_eqauls(key)
        r = res['Items'][0]
        response[i] = {'short_description': r['short_description'], 'link': r['link']}
        i+=1
    
    return response

def pruneList(list,phraseList):  #putting weight on results
    seen = {}
    final = {}
    for x in list:
        if x not in seen.keys() and x not in final.keys(): #check if a duplicate
            final[x] = 1
        if x in seen.keys() and x in final.keys():
            final[x] += 1        
        seen[x] = 1
    
    intersection = False
    
    for v in final.values():
        if v in range(2 , 9):
            intersection = True
            
    if not intersection:
        if len(final) == 0:         # if final is empty that means there are no results
            print("Sorry. There are no results for that")
        
        if len(phraseList) >= 2:    # if 2 or more words do not have an intersection 
            print("We could not find anything for that, but here are some related results.")
        
        # if there is only one word in the phraseList nothing will print 
        
    return final

def query_table_eqauls(filter_value=None):
    
    dynamodb_resource = boto3.resource('dynamodb')   
   
    table = dynamodb_resource.Table('Senior_Design_Table')

    if filter_value:
        filtering_exp = Key('short_description').eq(filter_value)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
        
    #for i in response['Items']:
        #print(i['short_description'])
        #print(i['link'])
        #print()

    return response
    
        
def scan_table():
    dynamodb_resource = boto3.resource('dynamodb')   
   
    table = dynamodb_resource.Table('Senior_Design_Table')
    
    response = table.scan()
    
    return response

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': err.message if err else json.dumps(res)
    }


def lambda_handler(event, context):
    
    
    res = search(event['query'])
    
    return respond(None, res)
  

