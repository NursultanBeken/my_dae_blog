import os
import json
import boto3
import botocore
from boto3.dynamodb.types import TypeDeserializer
deser = TypeDeserializer()

DYNAMO_DB_NAME = os.getenv("DYNAMO_DB_NAME","prod-dynamodb-table")
CREDS_PARAMETER_PATH = os.getenv("CREDS_PARAMETER_PATH","/master/prod/avm/govcreds")
TEST_FLG = os.getenv("TEST_FLG", "0")


def get_creds(path, session):
    """Retrive AWS credentials from parameter store
    """

    client = session.client("ssm")
    response = client.get_parameters(
        Names=[path],
        WithDecryption=True 
    )

    return json.loads(response["Parameters"][0]["Value"])

comm_session = boto3.Session()
prod_creds = get_creds(CREDS_PARAMETER_PATH, comm_session)

# init prod session
if TEST_FLG == "1":
    prod_session = boto3.Session()
else:
    prod_session = boto3.Session()
    prod_session = boto3.Session(
        aws_access_key_id=prod_creds["id"],
        aws_secret_access_key=prod_creds["key"],
        region_name="us-east-1"
    )

dynamodb = prod_session.resource("dynamodb")
table = dynamodb.Table(DYNAMO_DB_NAME)

def handler(event, context):
    """Handler
    """
    for record in event["Records"]:
        if record["eventSource"] == "aws:dynamodb" and record["awsRegion"] == "us-east-1":

            if record["eventName"] in ["MODIFY", "INSERT"]:
                # update item in the replica
                data = { k: deser.deserialize(v) for k,v in record["dynamodb"]["NewImage"].items() }
                put_record(table, data)
                continue

            if record["eventName"] == "REMOVE":
                key = { k: deser.deserialize(v) for k,v in record["dynamodb"]["Keys"].items() }
                delete_record(table, key)
                continue


def put_record(table, data):
    """Put records into replica DynamoDb
    """
    try:
        response = table.put_item(Item=data)
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])


def delete_record(table, key):
    """Delete records into replica DynamoDb
    """
    try:
        response = table.delete_item(Key=key)
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])