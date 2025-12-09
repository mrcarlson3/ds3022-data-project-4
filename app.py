import os
import boto3
import json
from chalice import Chalice
from botocore.exceptions import ClientError

app = Chalice(app_name='s3-events')
app.debug = True

# Set the values in the .chalice/config.json file.
S3_BUCKET = os.environ.get('APP_BUCKET_NAME', '')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', '')


@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'], suffix='.json')
def s3_handler(event):
<<<<<<< HEAD
    # get the event, pull the file from s3, read it, and insert into DDB
    app.log.debug(f"Received event for bucket: {event.bucket} key: {event.key}")
    # get the object from s3
    data = get_s3_object(event.bucket, event.key)
    # insert into DDB
    insert_data_into_dynamodb(data)

    return data

def get_s3_object(bucket, key):
    # get the object from s3
=======
    app.log.debug(f"Received bucket event: {event.bucket}, key: {event.key}")
    data = get_s3_object(event.bucket, event.key)
    insert_data_into_dynamodb(data)
    return data

def get_s3_object(bucket, key):
>>>>>>> upstream/main
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(e)

def insert_data_into_dynamodb(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    try:
        response = table.put_item(
            Item={
                'event_key': data['event_key'],
                'building_code': data['building_code'],
                'building_door_id': data['building_door_id'],
                'access_time': data['access_time'],
                'user_identity': data['user_identity']
            }
        )
        app.log.debug(f"DynamoDB response: {response}")
        return response
    except Exception as e:
        app.log.error(f"Error inserting data into DynamoDB: {e}")
        raise e

@app.route('/access', methods=['GET'])
def get_access():
<<<<<<< HEAD
    # return all records from DDB
=======
>>>>>>> upstream/main
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    try:
        items = table.scan()['Items']
        sorted_items = sorted(items, key=lambda x: x['access_time'])
        return sorted_items
    except ClientError as e:
<<<<<<< HEAD
        raise e
=======
        app.log.error(f"Error scanning DynamoDB table: {e}")
        raise e
>>>>>>> upstream/main
