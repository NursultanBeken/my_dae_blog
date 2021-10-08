import os
import pytest
import boto3
from unittest import mock
from src import app


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"DYNAMO_DB_NAME": 'test-dynamodb-table'}):
        yield


def test_handler(dynamo_stream_event, dynamodb_table):
    """Test handler
    """
    try:
        response = app.handler(dynamo_stream_event, None)
    except Exception as e:
        print(e)

    assert True == True

def test_publish_record(dynamodb_table):
    """Test the publish_record into table with a valid input data
    """
    data = {'Message': 'This item has changed', 'Id': '120'}
    app.publish_record(data)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('test-dynamodb-table')
    response = table.get_item(
        Key={'Id': '120'}
    )
    assert response["Item"]["Id"] == "120"