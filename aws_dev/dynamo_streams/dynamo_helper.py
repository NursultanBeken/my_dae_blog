import os
from decimal import Decimal
import json
import boto3
from pprint import pprint
from botocore.exceptions import ClientError

DYNAMO_DB_NAME = os.environ.get("DYNAMO_DB_NAME","test-replica-db-table")

def load_items(accounts):

    session = boto3.session.Session(profile_name="dev",region_name="us-east-1")
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(DYNAMO_DB_NAME)

    for account in accounts:
        table.put_item(Item=account)


def get_account(account_id, partition):

    session = boto3.session.Session()
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table(DYNAMO_DB_NAME)

    try:
        response = table.get_item(Key={'account_id': account_id, 'partition': partition})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

if __name__ == '__main__':
    with open("accounts.json") as json_file:
        accounts_list = json.load(json_file, parse_float=Decimal)
    
    load_items(accounts_list)
    # account = get_account("123456", "aws")
    # if account:
    #     print("Get account succeeded:")
    #     pprint(account, sort_dicts=False)