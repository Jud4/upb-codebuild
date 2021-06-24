import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

users_table = os.environ['MOVIES_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getRoom(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # /cinema_rooms/{room_id}
    array_path = path.split("/") # ["", "user", "123"]
    room_id = array_path[-1]
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(room_id)
    )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
    
def putRoom(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"] # /cinema_rooms/{room_id}
    array_path = path.split("/") # ["", "user", "123"]
    room_id = array_path[-1]
    
    body = event["body"] #"{\n\t\"name\": \"Jack\",\n\t\"last_name\": \"Click\",\n\t\"age\": 21\n}"
    body_object = json.loads(body)
    
    people_array = body_object['customers']
    movie_id = body_object['movie_id']
    date = body_object['date']
    
    response = table.get_item(
        Key={
            'pk': room_id,
            'sk': room_id
        }
    )
    item = response['Item']
    
    seats_available = int(item['seats_available'])
    
    if len(people_array) > seats_available:
        return{
            'statusCode': 409,
            'body': json.dumps('There are not enough seats in this cinema room')
        }
    seats_available = seats_available - len(people_array)
    
    table.update_item(
        Key={
            'pk': room_id,
            'sk': room_id
        },
        UpdateExpression='SET seats_available = :val1',
        ExpressionAttributeValues={
            ':val1': str(seats_available)
        }
    )
    
    for person in people_array:
        table.put_item(
            Item={
                'pk': f"{movie_id}_{room_id}_{date}",
                'sk': person,
                'customer': person,
                'date': date
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }