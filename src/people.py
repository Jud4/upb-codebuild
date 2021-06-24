import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['MOVIES_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getPeople(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    # "pathParameters" -> "room_id"
    # "pathParameters" -> "movie_id"
    # "multiValueQueryStringParameters" -> "date" -> [0]
    
    room_id = event["pathParameters"]["room_id"]
    movie_id = event["pathParameters"]["movie_id"]
    date = event["multiValueQueryStringParameters"]["date"][0]
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(f"{movie_id}_{room_id}_{date}")
    )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
    
def getPerson(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/user/123"
    array_path = path.split("/") # ["", "user", "123"]
    customer_id = array_path[-1]
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(customer_id)
    )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
