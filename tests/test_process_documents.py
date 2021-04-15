import json
import os
import boto3
from moto import mock_s3, mock_dynamodb2
import pytest

mock_event_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '../events/mock_event.json')
mock_event_data = open(mock_event_file)
mock_event = json.load(mock_event_data)

MOCK_BUCKET_NAME = 'mock-bucket'
MOCK_OBJECT_NAME = 'mock-patent.pdf'


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials"""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture()
def s3(aws_credentials):
    """Pytest fixture which creates a mock
    s3 bucket and yields a fake boto3 s3 client
    """
    with mock_s3():
        s3 = boto3.client("s3", region_name='us-east-1')
        s3.create_bucket(Bucket=MOCK_BUCKET_NAME)
        yield s3

@pytest.fixture()
def dynamodb(aws_credentials):
    """Pytest fixture which creates a mock
    dynamodb database and yields a fake boto3 dynamodb client
    """
    with mock_dynamodb2():
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        dynamodb.create_table(TableName='patents-dev',
        KeySchema=[
            {
                'AttributeName': 'patentNumber',
                'KeyType': 'HASH'  # Partition key
            }],  AttributeDefinitions=[
            {
                'AttributeName': 'patentNumber',
                'AttributeType': 'N'
            }])
        dynamodb.create_table(TableName='bioMolecules-dev',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  # Partition key
            }],  AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'N'
            }])
        yield dynamodb


def test_handle_event(s3, dynamodb):
    from src.process_documents import app
    s3.put_object(Bucket=MOCK_BUCKET_NAME, Key=MOCK_OBJECT_NAME, Body="")
    handler_resp = app.lambda_handler(mock_event, context={})
    assert handler_resp == 'Success'
