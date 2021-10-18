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
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "NewImage":{
                        "Message":{
                            "S":"New item!"
                        },
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
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
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "NewImage":{
                        "Message":{
                            "S":"This item has changed"
                        },
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "OldImage":{
                        "Message":{
                            "S":"New item!"
                        },
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
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
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "OldImage":{
                        "Message":{
                            "S":"This item has changed"
                        },
                        "account_id":{
                            "S":"101"
                        },
                        "partition":{
                            "S": "aws"
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
                        "account_id":{
                            "S":"103"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "NewImage":{
                        "Message":{
                            "S":"This item has changed"
                        },
                        "account_id":{
                            "S":"103"
                        },
                        "partition":{
                            "S": "aws"
                        }
                    },
                    "OldImage":{
                        "Message":{
                            "S":"New item!"
                        },
                        "account_id":{
                            "S":"103"
                        },
                        "partition":{
                            "S": "aws"
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
def dynamodb_table(aws_credentials):
    with moto.mock_dynamodb2():
        boto3.client('dynamodb').create_table(
            AttributeDefinitions=[
                {'AttributeName': 'account_id', 'AttributeType': 'S'},
                {'AttributeName': 'partition', 'AttributeType': 'S'}
            ],
            TableName=TEST_DYNAMO_TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'account_id', 'KeyType': 'HASH'},
                {'AttributeName': 'partition', 'KeyType': 'RANGE'}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            }
        )
        yield boto3.resource('dynamodb').Table(TEST_DYNAMO_TABLE_NAME)


@pytest.fixture
def ssm_param(aws_credentials):
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
