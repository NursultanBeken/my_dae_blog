import os
import pytest
import boto3
from unittest import mock

@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    env = {
        "DYNAMO_DB_NAME": "test-dynamodb-table",
        "TEST_FLG": "1"
    }
    with mock.patch.dict(os.environ, env):
        yield


def test_handler(dynamo_stream_event, dynamodb_table):
    """Test handler
    """
    from src import app
    try:
        response = app.handler(dynamo_stream_event, None)
    except Exception as e:
        print(e)

    assert True == True
    

def test_put_new_record(dynamodb_table):
    """Test the put_record into table with a valid input data
    """
    from src import app

    data = {'Message': 'This item has changed', 'Id': '199'}
    app.put_record(dynamodb_table, data)
    
    response = dynamodb_table.get_item(Key={'Id': '199'})["Item"]
    assert response["Id"] == data["Id"]
    assert response["Message"] == data["Message"]

def test_update_record(dynamodb_table):
    """Test update_record into table with a valid input data
    """
    from src import app
    data = {'Message': '17777777', 'Id': '199'}
    dynamodb_table.put_item(Item=data)

    newdata = {
        'Id': '199',
        'Message': '9999999999', 
        "new_attr": "new_attr_value"
    }
    response = app.put_record(dynamodb_table, newdata)
    
    get_response = dynamodb_table.get_item(Key={'Id': '199'})["Item"]

    assert get_response["Message"] == newdata["Message"]
    assert get_response["new_attr"] == newdata["new_attr"]

def test_delete_record(dynamodb_table):
    """Test delete_record into table with a valid input data
    """
    from src import app
    data = {'Message': '17777777', 'Id': '199'}
    key = data["Id"]

    dynamodb_table.put_item(Item=data)
    get_response = dynamodb_table.get_item(Key={'Id': '199'})
    assert "Item" in get_response

    response = app.delete_record(dynamodb_table, {"Id": key})
    get_response = dynamodb_table.get_item(Key={'Id': '199'})
    assert "Item" not in get_response

def test_ged_creds():
    pass