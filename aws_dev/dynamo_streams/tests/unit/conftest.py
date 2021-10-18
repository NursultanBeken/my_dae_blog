# conftest.py
import os
import pytest
import moto
import boto3

TEST_DYNAMO_TABLE_NAME = 'test-dynamodb-table'

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture()
def dynamo_stream_event():
    """ Generates DynamoDb stream Event"""
    return {
        "Records":[
            {
                "eventID":"1",
                "eventName":"INSERT",
                "eventVersion":"1.0",
                "eventSource":"aws:dynamodb",
                "awsRegion":"us-east-1",
                "dynamodb":{
                    "Keys":{
                    "Id":{
                        "S":"101"
                    }
                    },
                    "NewImage":{
                    "Message":{
                        "S":"New item!"
                    },
                    "Id":{
                        "S":"101"
                    }
                    },
                    "SequenceNumber":"111",
                    "SizeBytes":26,
                    "StreamViewType":"NEW_AND_OLD_IMAGES"
                },
                "eventSourceARN":"stream-ARN"
            },
            {
                "eventID":"2",
                "eventName":"MODIFY",
                "eventVersion":"1.0",
                "eventSource":"aws:dynamodb",
                "awsRegion":"us-east-1",
                "dynamodb":{
                    "Keys":{
                    "Id":{
                        "S":"101"
                    }
                    },
                    "NewImage":{
                    "Message":{
                        "S":"This item has changed"
                    },
                    "Id":{
                        "S":"101"
                    }
                    },
                    "OldImage":{
                    "Message":{
                        "S":"New item!"
                    },
                    "Id":{
                        "S":"101"
                    }
                    },
                    "SequenceNumber":"222",
                    "SizeBytes":59,
                    "StreamViewType":"NEW_AND_OLD_IMAGES"
                },
                "eventSourceARN":"stream-ARN"
            },
            {
                "eventID":"3",
                "eventName":"REMOVE",
                "eventVersion":"1.0",
                "eventSource":"aws:dynamodb",
                "awsRegion":"us-east-1",
                "dynamodb":{
                    "Keys":{
                    "Id":{
                        "S":"101"
                    }
                    },
                    "OldImage":{
                    "Message":{
                        "S":"This item has changed"
                    },
                    "Id":{
                        "S":"101"
                    }
                    },
                    "SequenceNumber":"333",
                    "SizeBytes":38,
                    "StreamViewType":"NEW_AND_OLD_IMAGES"
                },
                "eventSourceARN":"stream-ARN"
            },
            {
                "eventID":"4",
                "eventName":"MODIFY",
                "eventVersion":"1.0",
                "eventSource":"aws:dynamodb",
                "awsRegion":"us-gov-west-1",
                "dynamodb":{
                    "Keys":{
                    "Id":{
                        "S":"103"
                    }
                    },
                    "NewImage":{
                    "Message":{
                        "S":"This item has changed"
                    },
                    "Id":{
                        "S":"103"
                    }
                    },
                    "OldImage":{
                    "Message":{
                        "S":"New item!"
                    },
                    "Id":{
                        "S":"103"
                    }
                    },
                    "SequenceNumber":"222",
                    "SizeBytes":59,
                    "StreamViewType":"NEW_AND_OLD_IMAGES"
                },
                "eventSourceARN":"stream-ARN"
            }
        ]
    }

@pytest.fixture
def dynamodb_table():
    with moto.mock_dynamodb2():
        boto3.client('dynamodb').create_table(
            AttributeDefinitions=[
                {'AttributeName': 'Id', 'AttributeType': 'S'}
            ],
            TableName=TEST_DYNAMO_TABLE_NAME,
            KeySchema=[{'AttributeName': 'Id', 'KeyType': 'HASH'}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            }
        )
        yield boto3.resource('dynamodb').Table(TEST_DYNAMO_TABLE_NAME)


@pytest.fixture
def ssm_param():
    with moto.mock_ssm():
        client = boto3.client("ssm")
        client.put_parameter(
            Name="/master/test/avm/govcreds",
            Description="A test parameter", 
            Value="""{
                "id": "testing_id",
                "key": "testing_key"
            }""", 
            Type="SecureString"
        )
        yield
