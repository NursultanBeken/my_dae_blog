import os
import json
import boto3
import botocore
from boto3.dynamodb.types import TypeDeserializer
deser = TypeDeserializer()


def handler(event, context):
    """
    Handler
    """
    for record in event["Records"]:
        if record["eventSource"] == "aws:dynamodb" and record["eventName"] == "MODIFY":

            old_iamge = record["dynamodb"]["OldImage"]
            new_image = {k: deser.deserialize(v)  for k,v in record["dynamodb"]["NewImage"].items() }
            print(new_image)
            publish_record(new_image)


def publish_record(data):
    """Put records into replica DynamoDb in another account
    """
    DYNAMO_DB_NAME = os.getenv("DYNAMO_DB_NAME","prod-dynamodb-table")
    session = boto3.session.Session(profile_name="dev",region_name="us-east-1")
    dynamodb = session.resource("dynamodb")
    table = dynamodb.Table(DYNAMO_DB_NAME)
    print(f"DYNAMO_DB_NAME={DYNAMO_DB_NAME}")
    try:
        response = table.put_item(Item=data)
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])