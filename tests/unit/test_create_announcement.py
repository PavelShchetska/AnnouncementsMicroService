import json
import pytest
import boto3

from moto import mock_dynamodb2
from announcement_serverless import create_announcement

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "title": "Title",
        "description": "Description"
    }

@mock_dynamodb2
def test_create_announcement_lambda_handler(apigw_event, mocker):

    set_dynamodb()

    ret = create_announcement.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 200
    assert "Succesfully inserted announcement!" in ret["body"]

@mock_dynamodb2
def test_create_announcement_lambda_handler_exeption(apigw_event, mocker):

    ret = create_announcement.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert "Error saving the announcement" in ret["body"]

def set_dynamodb():
    client = boto3.client('dynamodb', region_name='us-east-1')
    client.create_table(
        TableName='announcements',
        KeySchema=[
            {
                'AttributeName': 'date',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 5
        }
    )
