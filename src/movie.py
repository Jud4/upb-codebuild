import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['MOVIES_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/user/123"
    array_path = path.split("/") # ["", "user", "123"]
    movie_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': movie_id
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
def putMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # "/user/123"
    array_path = path.split("/") # ["", "user", "123"]
    movie_id = array_path[-1]
    
    body = event["body"] #"{\n\t\"name\": \"Jack\",\n\t\"last_name\": \"Click\",\n\t\"age\": 21\n}"
    body_object = json.loads(body)
    
    
    table.put_item(
        Item={
            'pk': movie_id,
            'sk': movie_id,
            'title': body_object['title'],
            'actors': body_object['actors'],
            'year': body_object['year']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

def roomsPerDay(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    movie_id = event["pathParameters"]["movie_id"]
    date = event["multiValueQueryStringParameters"]["date"][0]

    response = table.query(
        KeyConditionExpression=Key('pk').eq(f"{movie_id}_{date}")
    )
    items = response['Items']
    print(items)

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
